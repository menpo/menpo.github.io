#!/usr/bin/env python
"""A small landmarker.io server for annotating a folder of images that have .pts files.

    python lmio_lite.py FOLDER [--port 5000] [--static DIR]

It speaks the landmarker.io API v2 (what the web client expects), serves the client from ``--static``
too, and stores the landmarks as the ``.pts`` files next to the images (pixels counted from 1, like menpo).
The first time an image is saved, the file it replaces is kept as ``NAME.original.pts``.
"""
import argparse
import io
import json
import mimetypes
import re
import shutil
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml
from PIL import Image

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
LM_ID = "ibug68"


def read_pts(path):
    body = Path(path).read_text().split("{")[1].split("}")[0]
    return [[float(v) for v in line.split()[:2]] for line in body.strip().splitlines()]


def write_pts(path, points):
    lines = "\n".join(f"{x:.3f} {y:.3f}" for x, y in points)
    Path(path).write_text(f"version: 1\nn_points: {len(points)}\n{{\n{lines}\n}}\n")


def template_json(template_file):
    groups = yaml.safe_load(Path(template_file).read_text())["groups"]
    labels, connectivity, offset = [], [], 0
    for group in groups:
        n = group["points"]
        for entry in group.get("connectivity", []):
            if ":" in entry:
                a, b = (int(v) for v in entry.split(":"))
                connectivity += [[i + offset, i + 1 + offset] for i in range(a, b)]
            else:
                a, b = (int(v) for v in entry.split())
                connectivity.append([a + offset, b + offset])
        labels.append({"label": group["label"], "mask": list(range(offset, offset + n))})
        offset += n
    return {"version": 2, "labels": labels, "landmarks": {"connectivity": connectivity, "points": [[None, None]] * offset}}


class Handler(BaseHTTPRequestHandler):
    folder: Path
    static: Path
    template: dict

    # ---- helpers
    def send(self, status, body=b"", mime="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, value, status=200):
        self.send(status, json.dumps(value).encode())

    def images(self):
        return sorted(p for p in self.folder.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES)

    def image_path(self, asset_id):
        for p in self.images():
            if p.stem == asset_id:
                return p
        return None

    def pts_path(self, asset_id):
        return self.folder / f"{asset_id}.pts"

    def landmark_json(self, asset_id):
        path = self.pts_path(asset_id)
        if not path.exists():
            return self.template
        points = [[y - 1, x - 1] for x, y in read_pts(path)]  # file: (x, y) from 1; client: (y, x) from 0, like menpo
        data = json.loads(json.dumps(self.template))
        data["landmarks"]["points"] = points
        return data

    # ---- routes
    def do_OPTIONS(self):
        self.send(204)

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        api = re.match(r"^/api/v2/(.*)$", path)
        if not api:
            return self.static_file(path)
        parts = [p for p in api.group(1).split("/") if p]
        try:
            if parts == ["mode"]:
                return self.send_json("image")
            if parts == ["collections"]:
                return self.send_json(["all"])
            if parts == ["collections", "all"]:
                return self.send_json([p.stem for p in self.images()])
            if parts == ["templates"]:
                return self.send_json([LM_ID])
            if parts == ["templates", LM_ID]:
                return self.send_json(self.template)
            if parts == ["images"]:
                return self.send_json([p.stem for p in self.images()])
            if parts[:1] == ["textures"] and len(parts) == 2:
                p = self.image_path(parts[1])
                return self.send(200, p.read_bytes(), mimetypes.guess_type(p.name)[0]) if p else self.send_json("no such image", 404)
            if parts[:1] == ["thumbnails"] and len(parts) == 2:
                p = self.image_path(parts[1])
                if not p:
                    return self.send_json("no such image", 404)
                im = Image.open(p).convert("RGB")
                im.thumbnail((200, 200))
                buffer = io.BytesIO()
                im.save(buffer, "JPEG")
                return self.send(200, buffer.getvalue(), "image/jpeg")
            if parts == ["landmarks"]:
                return self.send_json({p.stem: [LM_ID] for p in self.images() if self.pts_path(p.stem).exists()})
            if parts[:1] == ["landmarks"] and len(parts) == 2:
                return self.send_json([LM_ID] if self.pts_path(parts[1]).exists() else [])
            if parts[:1] == ["landmarks"] and len(parts) == 3:
                return self.send_json(self.landmark_json(parts[1]))
        except Exception as error:  # noqa: BLE001
            return self.send_json(str(error), 500)
        self.send_json("not found", 404)

    def do_PUT(self):
        path = unquote(urlparse(self.path).path)
        m = re.match(r"^/api/v2/landmarks/([^/]+)/([^/]+)$", path)
        if not m or not self.image_path(m.group(1)):
            return self.send_json("not found", 404)
        asset_id = m.group(1)
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        points = data["landmarks"]["points"]
        if len(points) != 68 or any(v is None for p in points for v in p):
            return self.send_json("all 68 points are needed", 409)
        target = self.pts_path(asset_id)
        original = self.folder / f"{asset_id}.original.pts"
        if target.exists() and not original.exists():
            shutil.copy2(target, original)
        write_pts(target, [[p[1] + 1, p[0] + 1] for p in points])  # the client sends (y, x)
        self.send_json("success")

    def static_file(self, path):
        rel = path.lstrip("/") or "index.html"
        target = (self.static / rel).resolve()
        if self.static.resolve() not in target.parents and target != self.static.resolve() or not target.is_file():
            return self.send(404, b"not found", "text/plain")
        self.send(200, target.read_bytes(), mimetypes.guess_type(target.name)[0] or "application/octet-stream")

    def log_message(self, fmt, *args):
        sys.stderr.write("%s\n" % (fmt % args))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--static", default=str(Path(__file__).parent / "static"))
    parser.add_argument("--template", default=str(Path(__file__).parent / "ibug68.yml"))
    args = parser.parse_args()
    Handler.folder = Path(args.folder)
    Handler.static = Path(args.static)
    Handler.template = template_json(args.template)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"landmarker.io at http://127.0.0.1:{args.port}/?server=http://127.0.0.1:{args.port}  ({len(Handler.images(Handler))} images)", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
