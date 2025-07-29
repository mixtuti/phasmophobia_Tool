import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QGroupBox, QGridLayout, QComboBox, QScrollArea, QTextEdit
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

# ----------------------------
# JSONファイルの埋め込み対応
# ----------------------------
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

json_path = os.path.join(base_path, "ghosts.json")
icon_path = os.path.join(base_path, "ghost.ico")

# ゴーストデータ読み込み
with open(json_path, encoding="utf-8") as f:
    ghosts = json.load(f)

# 証拠・特徴の説明
explanations = {
    "EMFレベル5": "高レベルの電磁波反応。ゴーストの干渉や現象時に検出される。",
    "スピリットボックス": "特定の質問にゴーストが声で応答する装置。",
    "ゴーストライティング": "置かれたブックにゴーストが文字を書き残す現象。",
    "ゴーストオーブ": "カメラ越しに白く小さい光の玉が漂う現象。",
    "氷点下の温度": "温度計で0℃未満、息が白くなる現象。",
    "D.O.T.S.プロジェクター": "緑色のレーザーにゴーストのシルエットが映る。",
    "指紋": "UVライトで扉や窓に指紋、塩を踏むと足跡が残る。",

    # 移動・足音系
    "足音が遅い": "特定条件下でのみ移動速度が遅くなる。",
    "足音が速い": "ゴーストの移動速度が特定条件下で速い。",
    "視認加速をしない": "プレイヤーに見られても移動速度が変わらない。",
    "部屋を移動しない": "ゴーストルームから離れずに行動する。",
    "2種類の速度": "同時に異なる速度で動くゴーストが存在するように見える。",
    "視界内加速": "プレイヤーに見られると移動速度が上がる。",
    "遠距離高速・近距離低速": "遠距離では速く、近距離では遅い移動をする。",
    "電子機器高速化": "電子機器の近くで移動速度が上がる。",
    "老化": "時間が経つと移動速度が低下する。",
    "ワープ移動": "プレイヤーの近くへ瞬間移動することがある。",
    "気温依存": "室温によって移動速度が変化する。",
    "正気度依存": "プレイヤーの正気度によって移動速度が変わる。",
    "足音の範囲が狭い": "ゴーストの足音の聞こえる範囲が狭い",

    # ハント系
    "頻繁にハント": "通常よりも高い頻度でハントを仕掛ける。",
    "十字架が効く": "十字架でハントを阻止できる。",
    "火を消す": "キャンドルやライターの火を吹き消す。",
    "浄化香の効果時間が短い": "スマッジスティックの効果が通常より短い。",
    "浄化香の効果時間が180秒": "スマッジスティックの効果が通常より長い（180秒）。",
    "点滅間隔が長い": "ハント中に姿が見える時間が長い。",
    "特定条件でハント": "特殊な条件下でハントを開始できる。",
    "ターゲット固定": "特定のプレイヤーのみを狙う。",
    "実体化長い": "ハント中に実体化している時間が長い。",

    # 超常現象系
    "超常現象が多い": "干渉や現象が頻繁に発生する。",
    "ゴーストミストが起きない": "ゴーストミストの現象を全く起こさない。",
    "歌を歌わない": "歌の超常現象が一切発生しない。",
    "頻繁に歌う": "歌の超常現象がよく発生する。",
    "正気度減少（特殊）": "特定の現象で正気度が大きく減少する。",
    "同時干渉": "複数の物を同時に干渉・投げることがある。",
    "ブレーカーオンにしない": "ブレーカーを自発的に着けない。",
    "ブレーカーオフにしない": "ブレーカーを自発的に落とさない。",
    "電気を付けない": "電気のスイッチを入れない行動をとる。",
    "電球破壊": "電球を壊す現象を起こす。",
    "電気を即消す": "プレイヤーが付けた電気をすぐに消す。",
    "消極的": "プレイヤーが近くにいると干渉やハントを行わない。",
    "遠距離干渉": "ゴーストのいる部屋以外で干渉を行うことがある。",

    # 証拠系
    "塩を踏まない": "塩を踏まず足跡が残らない。",
    "写真を撮ると消える": "写真撮影で一時的に姿が消える。",
    "特殊ボイス": "スピリットボックスで特殊な声が聞こえる。",
    "特殊なD.O.T.S.視認性": "特定条件下でのみD.O.T.S.に映る。",
    "指紋変化": "指紋の形や本数が変わることがある。",
    "ゴーストオーブ": "証拠に加えてゴーストオーブが発生する。",
    "近距離音反応": "近距離でのみ音に反応する。"
}

# 証拠一覧
evidence_list = [
    "EMFレベル5", "スピリットボックス", "ゴーストライティング",
    "ゴーストオーブ", "氷点下の温度", "D.O.T.S.プロジェクター", "指紋"
]

# 特徴カテゴリ
trait_categories = {
    "移動・足音系": [
        "足音が遅い", "足音が速い", "視認加速をしない", "部屋を移動しない",
        "2種類の速度", "視界内加速", "遠距離高速・近距離低速", "足音の範囲が狭い",
        "電子機器高速化", "老化", "ワープ移動", "気温依存", "正気度依存"
    ],
    "ハント系": [
        "頻繁にハント", "十字架が効く", "火を消す",
        "浄化香の効果時間が短い", "浄化香の効果時間が180秒",
        "点滅間隔が長い", "特定条件でハント", "ターゲット固定", "実体化長い"
    ],
    "超常現象系": [
        "超常現象が多い", "ゴーストミストが起きない", "歌を歌わない",
        "頻繁に歌う", "正気度減少（特殊）", "同時干渉",
        "ブレーカーオフにしない", "電気を付けない", "電球破壊",
        "電気を即消す", "消極的", "遠距離干渉", "怪奇音が頻繁"
    ],
    "証拠系": [
        "塩を踏まない", "写真を撮ると消える", "特殊ボイス", "怪奇音が頻繁",
        "特殊なD.O.T.S.", "指紋変化", "ゴーストオーブ", "近距離音反応", "他ゴースト模倣",
        "確定スピボ", "確定紫外線", "確定氷点下", "確定D.O.T.S."
    ]
}

# 選択状態
selected_evidence = set()
excluded_evidence = set()
selected_traits = set()
excluded_traits = set()

class CollapsibleBox(QGroupBox):
    """折りたたみ可能なカテゴリボックス"""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setTitle("")
        self.toggle_button = QPushButton(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.clicked.connect(self.toggle_content)

        self.content_area = QWidget()
        self.content_area.setVisible(False)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(3)
        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.content_area)

        self.content_layout = QGridLayout()
        self.content_layout.setSpacing(5)
        self.content_area.setLayout(self.content_layout)

    def toggle_content(self):
        self.content_area.setVisible(self.toggle_button.isChecked())

class GhostHelper(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phasmophobia ゴースト判別ツール")
        self.resize(1000, 600)
        self.setWindowIcon(QIcon(icon_path))
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        # 証拠・特徴ボタン管理
        self.evidence_buttons = {}
        self.trait_buttons = {}

        # 左パネル
        self.left_scroll = QScrollArea()
        self.left_scroll.setWidgetResizable(True)
        self.layout.addWidget(self.left_scroll, 1)

        left_container = QWidget()
        self.left_scroll.setWidget(left_container)
        self.left_panel = QVBoxLayout(left_container)

        self.create_evidence_buttons()
        self.create_trait_categories()
        self.create_sanity_selector()

        # 📖 解説エリア
        self.explanation_box = QTextEdit()
        self.explanation_box.setReadOnly(True)
        self.explanation_box.setFixedHeight(180)
        self.left_panel.addWidget(QLabel("📖 選択中/除外中の解説"))
        self.left_panel.addWidget(self.explanation_box)

        self.left_panel.addStretch()

        # 右パネル
        self.right_panel = QVBoxLayout()
        self.layout.addLayout(self.right_panel, 2)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.right_panel.addWidget(QLabel("候補ゴースト"))
        self.right_panel.addWidget(self.scroll_area)

        self.ghost_widget = QWidget()
        self.ghost_grid_layout = QGridLayout()
        self.ghost_grid_layout.setSpacing(8)
        self.ghost_widget.setLayout(self.ghost_grid_layout)
        self.scroll_area.setWidget(self.ghost_widget)

        self.detail_box = QTextEdit()
        self.detail_box.setReadOnly(True)
        self.right_panel.addWidget(QLabel("ゴースト詳細"))
        self.right_panel.addWidget(self.detail_box)

        # 言語切替とリセット
        lang_reset_layout = QHBoxLayout()
        self.lang_button = QPushButton("日本語⇔English")
        self.lang_button.clicked.connect(self.switch_language)
        lang_reset_layout.addWidget(self.lang_button)

        self.reset_button = QPushButton("リセット")
        self.reset_button.clicked.connect(self.reset_all)
        lang_reset_layout.addWidget(self.reset_button)

        self.right_panel.addLayout(lang_reset_layout)

        self.current_lang = "jp"
        self.update_ghost_list()

    def create_evidence_buttons(self):
        box = QGroupBox("証拠")
        grid = QGridLayout()
        box.setLayout(grid)
        self.left_panel.addWidget(box)
        for i, ev in enumerate(evidence_list):
            btn = QPushButton(ev)
            btn.clicked.connect(lambda _, ev=ev, b=btn: self.toggle_button(ev, b, "evidence"))
            grid.addWidget(btn, i // 2, i % 2)
            self.evidence_buttons[ev] = btn

    def create_trait_categories(self):
        for category_name, traits in trait_categories.items():
            box = CollapsibleBox(category_name)
            self.left_panel.addWidget(box)
            for i, tr in enumerate(traits):
                btn = QPushButton(tr)
                btn.clicked.connect(lambda _, tr=tr, b=btn: self.toggle_button(tr, b, "trait"))
                box.content_layout.addWidget(btn, i // 2, i % 2)
                self.trait_buttons[tr] = btn

    def create_sanity_selector(self):
        box = QGroupBox("ハント開始正気度")
        vbox = QVBoxLayout()
        self.sanity_combo = QComboBox()
        self.sanity_combo.addItem("すべて")
        self.sanity_combo.addItems(["35%以下", "40%以下", "50%以下", "60%以下", "70%以下", "特殊"])
        self.sanity_combo.currentIndexChanged.connect(self.update_ghost_list)
        vbox.addWidget(self.sanity_combo)
        box.setLayout(vbox)
        self.left_panel.addWidget(box)

    def toggle_button(self, name, button, category):
        if button.styleSheet() == "":
            button.setStyleSheet("color: blue; font-weight: bold;")
            (selected_evidence if category == "evidence" else selected_traits).add(name)
        elif "blue" in button.styleSheet():
            button.setStyleSheet("color: red; text-decoration: line-through;")
            if category == "evidence":
                selected_evidence.discard(name)
                excluded_evidence.add(name)
            else:
                selected_traits.discard(name)
                excluded_traits.add(name)
        else:
            button.setStyleSheet("")
            if category == "evidence":
                excluded_evidence.discard(name)
            else:
                excluded_traits.discard(name)
        self.update_ghost_list()
        self.update_explanations()

    def update_explanations(self):
        """現在の選択・除外状態の説明を表示"""
        text = ""
        if selected_evidence or selected_traits:
            text += "✅ **選択中:**\n"
            for name in selected_evidence | selected_traits:
                desc = explanations.get(name, "(説明未登録)")
                text += f"・{name}: {desc}\n"
        if excluded_evidence or excluded_traits:
            text += "\n❌ **除外中:**\n"
            for name in excluded_evidence | excluded_traits:
                desc = explanations.get(name, "(説明未登録)")
                text += f"・{name}: {desc}\n"
        if not text:
            text = "📖 現在選択・除外されている証拠・特徴はありません。"
        self.explanation_box.setPlainText(text)

    def update_ghost_list(self):
        # ゴースト一覧クリア
        for i in reversed(range(self.ghost_grid_layout.count())):
            widget = self.ghost_grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        width = self.scroll_area.viewport().width()
        col_width = 160
        columns = max(1, width // col_width)

        sanity_filter = self.sanity_combo.currentText()
        candidates = []
        for ghost_key, data in ghosts.items():
            if selected_evidence and not selected_evidence <= set(data["evidence"]):
                continue
            if excluded_evidence and excluded_evidence & set(data["evidence"]):
                continue
            if selected_traits and not selected_traits <= set(data.get("tags", [])):
                continue
            if excluded_traits and excluded_traits & set(data.get("tags", [])):
                continue
            if sanity_filter != "すべて" and sanity_filter not in data["hunt_sanity"]:
                if sanity_filter != "特殊" or "特殊" not in data["hunt_sanity"]:
                    continue

            name = ghost_key if self.current_lang == "en" else data["name_jp"]
            candidates.append((name, ghost_key))

        for i, (name, key) in enumerate(candidates):
            btn = QPushButton(name)
            btn.setFixedSize(QSize(140, 40))
            btn.clicked.connect(lambda _, key=key: self.show_ghost_details(key))
            self.ghost_grid_layout.addWidget(btn, i // columns, i % columns)

        self.write_status_to_json()

    def write_status_to_json(self):
        status = {
            "selected": list(selected_evidence | selected_traits),
            "excluded": list(excluded_evidence | excluded_traits),
            "candidates": []
        }

        sanity_filter = self.sanity_combo.currentText()
        for ghost_key, data in ghosts.items():
            if selected_evidence and not selected_evidence <= set(data["evidence"]):
                continue
            if excluded_evidence and excluded_evidence & set(data["evidence"]):
                continue
            if selected_traits and not selected_traits <= set(data.get("tags", [])):
                continue
            if excluded_traits and excluded_traits & set(data.get("tags", [])):
                continue
            if sanity_filter != "すべて" and sanity_filter not in data["hunt_sanity"]:
                if sanity_filter != "特殊" or "特殊" not in data["hunt_sanity"]:
                    continue

            name = data["name_jp"]
            status["candidates"].append(name)

        try:
            output_path = os.path.join(os.getcwd(), "ghost_output.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(status, f, ensure_ascii=False, indent=2)
            print(f"✅ ghost_output.json を保存しました: {output_path}")
        except Exception as e:
            print(f"❌ ファイル保存エラー: {e}")


    def show_ghost_details(self, ghost_key):
        data = ghosts[ghost_key]
        details = f"👻 ゴースト名: {data['name_jp']} ({data['name_en']})\n"
        details += f"🎯 ハント開始正気度: {data['hunt_sanity']}\n"
        details += f"✨ 特殊能力: {data['special']}\n📜 特徴:\n"
        for f in data["features"]:
            details += f"  ・{f}\n"
        details += "📖 証拠:\n"
        for e in data["evidence"]:
            details += f"  ・{e}\n"
        self.detail_box.setPlainText(details)

    def reset_all(self):
        selected_evidence.clear()
        excluded_evidence.clear()
        selected_traits.clear()
        excluded_traits.clear()
        for btn in self.evidence_buttons.values():
            btn.setStyleSheet("")
        for btn in self.trait_buttons.values():
            btn.setStyleSheet("")
        self.sanity_combo.setCurrentIndex(0)
        self.detail_box.clear()
        self.explanation_box.clear()
        self.update_ghost_list()
        self.write_status_to_json()

    def switch_language(self):
        self.current_lang = "en" if self.current_lang == "jp" else "jp"
        self.update_ghost_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GhostHelper()
    window.show()
    sys.exit(app.exec_())

# cd "C:\Users\mixtu\Downloads\ghost"
# pyinstaller --onefile --windowed --add-data "ghosts.json;." --icon=ghost.ico ghost.py