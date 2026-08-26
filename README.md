# From Simulation Benchmarks to Real-World Robot Learning

**CoRL 2026 Workshop** · Half-Day · November 12, 2026 · Austin, Texas, USA

[![Workshop Website](https://img.shields.io/badge/Website-Live-2563eb?style=flat-square&logo=github)](https://zhenzhenli820.github.io/corl2026-realworld-robot-learning/)
[![CoRL 2026](https://img.shields.io/badge/CoRL-2026-1a3a5c?style=flat-square)](https://www.corl.org)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey?style=flat-square)](https://creativecommons.org/licenses/by/4.0/)

---

## Overview

Simulation has become the engine of modern embodied AI. Physics-grounded environments like BEHAVIOR provide the scale, safety, and reproducibility that physical data collection cannot — enabling agents to develop high-level reasoning, long-horizon planning, and dexterous bimanual manipulation across thousands of everyday scenarios. Rigorous diagnostic frameworks like RoboEval further deepen what we can learn from simulation by instrumenting every task with stage-level metrics that reveal not just whether a policy succeeds, but precisely how and why it fails.

The frontier question is therefore not whether to train in simulation, but **how to ensure that the capabilities learned at scale in simulation carry over robustly to the physical world**. This workshop unites benchmark designers, robot-learning researchers, foundation-model developers, and real-robot practitioners to address that challenge together.

> *"Simulation is the most scalable training ground for embodied AI — how do we design benchmarks and evaluation protocols so that simulation-trained policies reliably transfer to real-world deployment?"*

---

## 🏆 CoRL 2026 Embodied AI Challenge Suite

Three complementary challenge tracks with independent leaderboards, codebases, and prize structures — unified by a shared evaluation protocol.

| Track | Name | Focus | Website |
|-------|------|--------|---------|
| 🏠 **Track 1** | BEHAVIOR Long-Horizon Household Challenge | Generalist agents in house-scale scenes; reasoning, navigation, bimanual manipulation | [behavior.stanford.edu](https://behavior.stanford.edu) |
| ♟️ **Track 2** | RoboChess Sim-to-Real Manipulation Challenge | GPU-accelerated sim training → real-world robot deployment across multiple embodiments | [corl-workshop-robochess](https://sites.google.com/view/corl-workshop-robochess) |
| 🤖 **Track 3** | RoboEval Diagnostic Bimanual Challenge | Stage-level failure diagnosis; outcome, efficiency, coordination, and safety metrics | [robo-eval.github.io](https://robo-eval.github.io) |

### Shared Cross-Track Metrics
All three tracks report a unified set of measures to enable cross-benchmark comparison:

`Outcome & Completion` · `Efficiency` · `Robustness` · `Safety` · `Compute Cost` · `Reproducibility`

---

## 📅 Important Dates

### Paper Track
| Milestone | Date |
|-----------|------|
| Submission Open | **August 26, 2026** |
| Paper Submission Deadline | **October 9, 2026** |
| Acceptance Notification | **October 23, 2026** |
| Final Schedule Announced | **November 1, 2026** |
| Workshop | **November 12, 2026** |

### Challenge Track
| Milestone | Date |
|-----------|------|
| Online Challenge Launch | See individual challenge pages |
| Submission Deadline | **October 16, 2026** |
| Winners Announcement | **November 4, 2026** |
| Leaderboard Updates | Rolling |

---

## 🎤 Invited Speakers

| Name | Affiliation | Status |
|------|-------------|--------|
| [Yashraj Narang](https://scholar.google.com/citations?user=M3NuG7AAAAAJ) | NVIDIA | In-Person |
| [Guannan Qu](https://www.guannanqu.com/) | Carnegie Mellon University | In-Person |
| [Yilun Du](https://yilundu.github.io/) | Harvard University | In-Person |
| [Chen Tang](https://scholar.google.com/citations?user=x78TL58AAAAJ) | UC Los Angeles | In-Person |

---

## 📝 Call for Papers

We invite short papers on simulation, benchmarking, and real-world robot learning, with particular interest in work that connects scalable evaluation in simulation to meaningful robot capabilities and real-world performance.

**Format:** short papers, up to 5 pages excluding references.

### Topics of Interest
- Simulation environments and benchmarks for scalable robot learning and evaluation
- Diagnostic and fine-grained evaluation, including capability metrics, failure analysis, robustness, and reproducibility
- Sim-to-real transfer and validation, including domain shift, adaptation, and studies connecting simulated and real-world performance
- Methods and empirical studies for challenging robot capabilities, including long-horizon, dexterous, bimanual, and generalist robot learning

We welcome new methods, benchmarks, challenge reports, empirical studies, negative results, and position papers that help clarify when and how simulation provides reliable evidence for real-world robot learning.

Submit via **[OpenReview](https://openreview.net/group?id=robot-learning.org/CoRL/2026/Workshop)**. Accepted papers will be presented as spotlights or posters with a strong emphasis on interactive discussion.

---

## 👥 Organizers

### General Organizers
| Name | Affiliation |
|------|-------------|
| [Zhenzhen Li](https://scholar.google.com/citations?user=6LYI6uUAAAAJ) | NVIDIA |
| [Yizhou Zhao](https://scholar.google.com/citations?user=l1h5kY8AAAAJ) | NVIDIA |
| [Jianwen Xie](https://scholar.google.com/citations?user=O3p4CIQAAAAJ) | Lambda |
| [Zijian (Leo) Du](https://scholar.google.com/citations?user=kfW01ekAAAAJ) | NVIDIA |
| [Ruohan Zhang](https://behavior.stanford.edu) | Northwestern University |
| [Huang (Raven) Huang](https://behavior.stanford.edu) | Stanford University |
| [Jiafei Duan](https://jiafei1224.github.io/) | NUS |
| [Jiajun Wu](https://jiajunwu.com/) | Stanford University |

### Track 1 & 3 — BEHAVIOR & RoboEval (Stanford & Partners)
Fei-Fei Li · Jiajun Wu · Ruohan Zhang · Huang Huang · Wensi Ai · Stef Ren · Cem Gokmen · Yalcin Tur · Minyeong Kim · Andi Xu · Lynn Jin · Brenda Chen · Sanjana Srivastava · Chengshu Li · Josiah Wong · Hang Yin · Yi Ru Wang · Jiafei Duan · Manling Li · Ranjay Krishna · Dieter Fox · Siddhartha Srinivasa · Carter Ung · Christopher Tan · Grant Tannert · Josephine Li · Amy Le · Rishabh Oswal · Markus Grotz · Wilbert Pumacay · Yuquan Deng

### Track 2 — RoboChess (NVIDIA & Partners)
Zhenzhen Li · Yizhou Zhao · Jianwen Xie · Zijian Du · Fangzhou Mu · Yuheng Li

---

## 🗓️ Workshop Schedule (Nov 12, 2026)

| Time | Session |
|------|---------|
| 8:50 – 9:00 | Opening Remarks |
| 9:00 – 9:30 | Keynote — Yashraj Narang (NVIDIA) |
| 9:30 – 10:00 | Keynote — Guannan Qu (Carnegie Mellon University) |
| 10:00 – 10:45 | Track 1 & 2 Challenge Awards & Spotlight — BEHAVIOR & RoboEval |
| 10:45 – 11:15 | Keynote — Yilun Du (Harvard University) |
| 11:15 – 11:45 | Keynote — Chen Tang (UC Los Angeles) |
| 11:45 – 12:15 | Track 3 Challenge Awards & Spotlight & Live Demo — RoboChess |
| 12:15 – 13:00 | Group Discussion & Poster Marketplace |

---

## 🌐 Website

The workshop website is built as a single-page static HTML site and hosted via GitHub Pages.

**Live site:** https://zhenzhenli820.github.io/corl2026-realworld-robot-learning/

To update the site, edit `index.html` and push to the `main` branch — GitHub Pages rebuilds automatically within ~1 minute.

```bash
git add index.html
git commit -m "your update message"
git push
```

---

## 📬 Contact

For questions about the workshop, please contact [zhenzhenl@nvidia.com](mailto:zhenzhenl@nvidia.com).

For challenge-specific questions, visit the individual challenge pages:
- [BEHAVIOR Challenge](https://behavior.stanford.edu)
- [RoboChess Challenge](https://sites.google.com/view/corl-workshop-robochess)
- [RoboEval Challenge](https://robo-eval.github.io)

---

## Citation

If you find this workshop or challenge suite useful in your research, please consider citing:

```bibtex
@workshop{corl2026_sim2real,
  title     = {From Simulation Benchmarks to Real-World Robot Learning},
  booktitle = {Workshop at Conference on Robot Learning (CoRL)},
  year      = {2026},
  month     = {November},
  address   = {Austin, Texas, USA},
  url       = {https://zhenzhenli820.github.io/corl2026-realworld-robot-learning/}
}
```

---

<p align="center">
  <b>CoRL 2026 Workshop</b> · From Simulation Benchmarks to Real-World Robot Learning<br/>
  November 12, 2026 · Austin, Texas, USA
</p>
