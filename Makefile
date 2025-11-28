# ==== Config ====
SRC_DIR := docs/20_design
OUT_DIR := $(SRC_DIR)/build
PUMLS   := $(wildcard $(SRC_DIR)/*.puml)
PNGS    := $(PUMLS:$(SRC_DIR)/%.puml=$(OUT_DIR)/%.png)
SVGS    := $(PUMLS:$(SRC_DIR)/%.puml=$(OUT_DIR)/%.svg)

PLANTUML_CMD ?= plantuml

# ==== Rules ====
.PHONY: all png svg clean

all: png svg

png: $(PNGS)
svg: $(SVGS)

$(OUT_DIR)/%.png: $(SRC_DIR)/%.puml | $(OUT_DIR)
	$(PLANTUML_CMD) -tpng -o build $<

$(OUT_DIR)/%.svg: $(SRC_DIR)/%.puml | $(OUT_DIR)
	$(PLANTUML_CMD) -tsvg -o build $<

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

clean:
	rm -f $(OUT_DIR)/*.png $(OUT_DIR)/*.svg