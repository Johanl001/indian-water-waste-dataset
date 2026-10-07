import os, sys, shutil

src, tag = sys.argv[1], sys.argv[2]
# dataset class id -> our class id (same order for this dataset)
id_map = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}

splits = {"train": "train", "valid": "val", "test": "test"}
kept = dropped = 0
for s_src, s_dst in splits.items():
    img_dir = os.path.join(src, s_src, "images")
    lab_dir = os.path.join(src, s_src, "labels")
    for img in os.listdir(img_dir):
        stem, ext = os.path.splitext(img)
        lab = os.path.join(lab_dir, stem + ".txt")
        lines = []
        if os.path.exists(lab):
            for line in open(lab):
                p = line.split()
                if p and int(p[0]) in id_map:
                    lines.append(" ".join([str(id_map[int(p[0])])] + p[1:]))
        if not lines:
            dropped += 1
            continue
        new = f"{tag}_{stem}"
        shutil.copy(os.path.join(img_dir, img), f"images/{s_dst}/{new}{ext}")
        open(f"labels/{s_dst}/{new}.txt", "w").write("\n".join(lines))
        kept += 1
print(f"kept {kept} images, dropped {dropped} with no labels")
