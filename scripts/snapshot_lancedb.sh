#!/bin/bash
# ============================================
# 倍斯特测试数据框架 - 快照管理
# 管理LanceDB向量库快照（支持回滚）
# 用法: bash snapshot_lancedb.sh save|list|restore
# ============================================
set -e
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SNAPSHOT_DIR="$PROJECT_DIR/data/mock/vector-data/snapshots"
VECTOR_DIR="$PROJECT_DIR/data/mock/vector-data"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$SNAPSHOT_DIR"

case "${1:-list}" in
    save)
        SNAPSHOT_NAME="${2:-snapshot_$TIMESTAMP}"
        SNAPSHOT_PATH="$SNAPSHOT_DIR/$SNAPSHOT_NAME"
        mkdir -p "$SNAPSHOT_PATH"
        # 复制向量数据
        if [ -d "$VECTOR_DIR" ] && [ "$(ls -A "$VECTOR_DIR" 2>/dev/null | grep -v snapshots | head -1)" ]; then
            for item in "$VECTOR_DIR"/*; do
                [ "$(basename "$item")" = "snapshots" ] && continue
                cp -r "$item" "$SNAPSHOT_PATH/"
            done
            echo "✅ 快照已保存: $SNAPSHOT_NAME"
        else
            echo "⚠️ 向量数据为空，快照为空"
        fi
        ;;
    list)
        echo "📋 可用快照列表:"
        if [ -d "$SNAPSHOT_DIR" ]; then
            for snap in "$SNAPSHOT_DIR"/*/; do
                if [ -d "$snap" ]; then
                    name=$(basename "$snap")
                    count=$(find "$snap" -type f 2>/dev/null | wc -l)
                    size=$(du -sh "$snap" 2>/dev/null | cut -f1)
                    echo "  📁 $name ($count 个文件, $size)"
                fi
            done
        else
            echo "  (无快照)"
        fi
        ;;
    restore)
        SNAPSHOT_NAME="${2:-}"
        if [ -z "$SNAPSHOT_NAME" ]; then
            echo "❌ 请指定要恢复的快照名称"
            echo "用法: bash snapshot_lancedb.sh restore <快照名称>"
            exit 1
        fi
        SNAPSHOT_PATH="$SNAPSHOT_DIR/$SNAPSHOT_NAME"
        if [ ! -d "$SNAPSHOT_PATH" ]; then
            echo "❌ 快照不存在: $SNAPSHOT_NAME"
            exit 1
        fi
        # 清理当前向量数据（保留snapshots目录）
        for item in "$VECTOR_DIR"/*; do
            [ "$(basename "$item")" = "snapshots" ] && continue
            rm -rf "$item"
        done
        # 恢复快照
        for item in "$SNAPSHOT_PATH"/*; do
            cp -r "$item" "$VECTOR_DIR/"
        done
        echo "✅ 已恢复快照: $SNAPSHOT_NAME"
        ;;
    *)
        echo "用法: bash snapshot_lancedb.sh save|list|restore [快照名称]"
        ;;
esac