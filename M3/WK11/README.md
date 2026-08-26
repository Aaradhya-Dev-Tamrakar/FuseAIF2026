# fuseAiF_wk11_vision_transformers

Week 11 — Computer Vision with Deep Learning · Fusemachines AI Fellowship

Business scenario: Computer Vision Engineer at QuickVision AI, replacing a ~45%-accuracy HSV colour-segmentation baseline across 500 warehouse cameras. Full spec in [`docs/W11_CV_Project_Guide.md`](docs/W11_CV_Project_Guide.md).

## Structure

```
.
├── notebooks/
│   └── W11_CV_Assignment_Notebook.ipynb   # main deliverable — 20 questions across 5 modules
├── docs/
│   └── W11_CV_Project_Guide.md            # assignment spec (role, dataset, walkthrough, checklist)
├── README.md
└── LICENSE
```

`resnet50_cifar10.onnx` (Q19 export, 94.2 MB) is generated at runtime and not committed — regenerate by running Q19.

## Modules

1. **CNN Classification** (Q1–Q5) — ResNet-50 transfer learning + GradCAM
2. **Object Detection** (Q6–Q9) — IoU, NMS, Faster R-CNN
3. **Segmentation** (Q10–Q13) — DeepLabv3+, pixel accuracy, mIoU, U-Net
4. **Generative — VAE** (Q14–Q16) — reparameterisation, ELBO, latent interpolation
5. **ViT + Deployment** (Q17–Q20) — patch embedding, CLIP zero-shot, ONNX export, deployment memo

## How to run

Colab or local with GPU recommended (Part 1 trains a ResNet-50 head; Part 4 trains a VAE from scratch).

```bash
pip install torch torchvision timm onnxruntime onnxscript
pip install git+https://github.com/openai/CLIP.git   # required for Q18
```

Run `notebooks/W11_CV_Assignment_Notebook.ipynb` top-to-bottom. CIFAR-10 auto-downloads (~170 MB) on first run.

## Status

**Complete — all 20 questions executed clean, all SELF-CHECKs pass, zero errors (Run 4).**

| Q | Result |
|---|---|
| Q1 | Output sizes correct (32, 30, 32, 112, 56) |
| Q3 | Val acc **74.1%** (epoch 3), 20,490 trainable params |
| Q6/Q8 | IoU/NMS correct |
| Q7 | bus.jpg: 5 detections · people.jpg: 3 detections |
| Q10 | bus.jpg → background/bus/car/person · people.jpg → background/person |
| Q11 | pixel_acc 1.0, mIoU 1.0 on synthetic perfect mask |
| Q14 | VAE 1,119,811 params; recon 170.7→87.5, KL 45.8→267.9 over 3 epochs |
| Q17 | Patch embed shape (4, 65, 256) ✓ |
| Q18 | CLIP zero-shot **92.0%** — real run, `openai-clip` installed |
| Q19 | ONNX exported, 94.2 MB, verified with onnxruntime |
| Q20 | Comparison table + memo, real numbers, accuracy-flip acknowledged |

**Note:** on this notebook's 200-image test slice, CLIP zero-shot (92.0%) outscored the fine-tuned ResNet-50 (74.1%) — the reverse of the typical zero-shot/supervised ordering. The Q20 memo's phased-deployment recommendation is driven by latency and explainability, not by an assumed accuracy edge; see the memo's Tradeoffs section.

### Bugs found and fixed during execution

- **Q4 (GradCAM)** — `cam.squeeze().cpu().numpy()` raised `RuntimeError: Can't call numpy() on Tensor that requires grad`. `cam` was built from hook-captured activations on an input with `requires_grad_(True)`, so it still carried a grad-tracking flag despite the earlier ReLU/normalize ops. Fixed by adding `.detach()` before `.numpy()`.
- **Q10 (DeepLabv3+ segmentation)** — `TypeError: Invalid shape (1, 390, 520, 3) for image data`. `seg_model(x)['out'].argmax(1)` retained the batch dimension (`(1, H, W)` instead of `(H, W)`), which then broadcast through `VOC_COLORS[mask]` and corrupted the overlay computation. Fixed with `.squeeze(0)` after `argmax`.
- **Q18 (CLIP zero-shot)** — silently fell to the scaffold's `acc_clip = 0.65` published-result stub because `openai-clip` was never installed, so the `try` block hit `except ImportError`. Added an install cell before Q18 (mirrors the Q19 onnxscript pattern) so CLIP runs for real; corrected result is 92.0%.

## License

MIT
