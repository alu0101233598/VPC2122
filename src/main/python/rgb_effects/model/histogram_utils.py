import io
from PIL import Image

alpha = 1.1

switchColorCode = {
  0: [(x / (255 * alpha), x / (255 * alpha), x / (255 * alpha)) for x in range(256)],
  1: [(x / 255, 0, 0) for x in range(256)],
  2: [(0, x / 255, 0) for x in range(256)],
  3: [(0, 0, x / 255) for x in range(256)]
}

def fig2img(fig):
  buf = io.BytesIO()
  fig.savefig(buf)
  buf.seek(0)
  img = Image.open(buf)
  return img
