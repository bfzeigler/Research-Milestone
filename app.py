"""A colorful, interactive PySide6 study-planning desktop app."""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QFormLayout, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QPushButton,
    QSpinBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

APP_STYLE = """
QMainWindow { background: #F4F7FF; }
QLabel#subtitle { color: #53617E; font-size: 14px; }
QFrame#card { background: white; border-radius: 14px; border: 1px solid #E1E7F5; }
QLineEdit, QComboBox, QSpinBox { background: #FFFFFF; color: #172033; border: 2px solid #AEBBE0; border-radius: 8px; padding: 8px; font-size: 14px; font-weight: 600; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border: 2px solid #6C63FF; }
QComboBox QAbstractItemView { background: white; color: #172033; selection-background-color: #DCD9FF; selection-color: #172033; }
QPushButton { background: #6C63FF; color: white; border: none; border-radius: 8px; padding: 9px 14px; font-weight: bold; }
QPushButton:hover { background: #584FE8; }
QPushButton#secondary { background: #E8E7FF; color: #443DAD; }
QPushButton#secondary:hover { background: #D9D7FF; }
QPushButton#danger { background: #FFE7EA; color: #B4233B; }
QPushButton#danger:hover { background: #FFD4DB; }
QTableWidget { background: white; color: #172033; border: 1px solid #C8D2EC; border-radius: 10px; gridline-color: #EDF0F8; font-size: 14px; }
QTableWidget::item { color: #172033; padding: 5px; }
QTableWidget::item:selected { background: #DCD9FF; color: #172033; }
QHeaderView::section { background: #EEF0FF; color: #443DAD; padding: 9px; border: none; font-weight: bold; }
QProgressBar { color: #172033; font-weight: bold; border: none; border-radius: 9px; background: #E7E9F7; text-align: center; min-height: 18px; }
QProgressBar::chunk { background: #31B99A; border-radius: 9px; }
"""


class StudyPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Planner")
        self.resize(760, 610)
        self.setStyleSheet(APP_STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        heading = QLabel("Study Planner ✨")
        heading.setStyleSheet("font-size: 29px; font-weight: bold; color: #252344;")
        layout.addWidget(heading)
        subtitle = QLabel("Plan your work, complete your tasks, and keep your study goal in sight.")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        goal_card = QFrame()
        goal_card.setObjectName("card")
        goal_layout = QVBoxLayout(goal_card)
        goal_layout.setContentsMargins(18, 14, 18, 14)
        goal_top = QHBoxLayout()
        self.goal_label = QLabel("Today's study goal")
        self.goal_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #252344;")
        self.goal_input = QSpinBox()
        self.goal_input.setRange(15, 600)
        self.goal_input.setValue(120)
        self.goal_input.setSuffix(" minute goal")
        self.goal_input.valueChanged.connect(self.update_summary)
        goal_top.addWidget(self.goal_label)
        goal_top.addStretch()
        goal_top.addWidget(self.goal_input)
        goal_layout.addLayout(goal_top)
        self.progress = QProgressBar()
        goal_layout.addWidget(self.progress)
        layout.addWidget(goal_card)

        input_card = QFrame()
        input_card.setObjectName("card")
        form = QFormLayout(input_card)
        form.setContentsMargins(18, 16, 18, 16)
        form.setSpacing(10)
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Example: Review Chapter 4")
        self.task_input.returnPressed.connect(self.add_task)
        self.minutes_input = QSpinBox()
        self.minutes_input.setRange(5, 600)
        self.minutes_input.setValue(30)
        self.minutes_input.setSuffix(" minutes")
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Example: Biology, History, or CSCE 490")
        label_style = "font-size: 14px; font-weight: bold; color: #172033;"
        task_label = QLabel("Task name:")
        task_label.setStyleSheet(label_style)
        subject_label = QLabel("School subject:")
        subject_label.setStyleSheet(label_style)
        minutes_label = QLabel("Planned study time:")
        minutes_label.setStyleSheet(label_style)
        form.addRow(task_label, self.task_input)
        form.addRow(subject_label, self.subject_input)
        form.addRow(minutes_label, self.minutes_input)
        layout.addWidget(input_card)

        buttons = QHBoxLayout()
        add_button = QPushButton("+ Add Task")
        add_button.clicked.connect(self.add_task)
        complete_button = QPushButton("✓ Mark Complete")
        complete_button.setObjectName("secondary")
        complete_button.clicked.connect(self.mark_complete)
        remove_button = QPushButton("Remove Selected")
        remove_button.setObjectName("secondary")
        remove_button.clicked.connect(self.remove_selected)
        clear_button = QPushButton("Clear All")
        clear_button.setObjectName("danger")
        clear_button.clicked.connect(self.clear_all)
        for button in (add_button, complete_button, remove_button, clear_button):
            buttons.addWidget(button)
        buttons.addStretch()
        layout.addLayout(buttons)

        self.task_table = QTableWidget(0, 4)
        self.task_table.setHorizontalHeaderLabels(["Task", "Category", "Minutes", "Status"])
        header = self.task_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.task_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.task_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.task_table.setAlternatingRowColors(True)
        layout.addWidget(self.task_table)

        self.summary = QLabel()
        self.summary.setAlignment(Qt.AlignRight)
        self.summary.setStyleSheet("font-weight: bold; color: #443DAD;")
        layout.addWidget(self.summary)
        self.update_summary()

    def add_task(self):
        task = self.task_input.text().strip()
        if not task:
            QMessageBox.warning(self, "Missing task", "Please enter a study task first.")
            return
        row = self.task_table.rowCount()
        self.task_table.insertRow(row)
        subject = self.subject_input.text().strip() or "General"
        values = [task, subject, str(self.minutes_input.value()), "Not started"]
        for column, value in enumerate(values):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter if column > 0 else Qt.AlignLeft | Qt.AlignVCenter)
            self.task_table.setItem(row, column, item)
        self.task_input.clear()
        self.subject_input.clear()
        self.task_input.setFocus()
        self.update_summary()

    def mark_complete(self):
        rows = sorted({index.row() for index in self.task_table.selectedIndexes()})
        if not rows:
            QMessageBox.information(self, "No selection", "Select one or more task rows to mark them complete.")
            return
        for row in rows:
            self.task_table.item(row, 3).setText("✓ Complete")
        self.update_summary()

    def remove_selected(self):
        selected_rows = sorted({index.row() for index in self.task_table.selectedIndexes()}, reverse=True)
        if not selected_rows:
            QMessageBox.information(self, "No selection", "Select a task row to remove it.")
            return
        for row in selected_rows:
            self.task_table.removeRow(row)
        self.update_summary()

    def clear_all(self):
        if self.task_table.rowCount() == 0:
            return
        if QMessageBox.question(self, "Clear tasks", "Remove every planned task?") == QMessageBox.Yes:
            self.task_table.setRowCount(0)
            self.update_summary()

    def update_summary(self):
        total = sum(int(self.task_table.item(row, 2).text()) for row in range(self.task_table.rowCount()))
        completed = sum(
            int(self.task_table.item(row, 2).text()) for row in range(self.task_table.rowCount())
            if self.task_table.item(row, 3).text() == "✓ Complete"
        )
        goal = self.goal_input.value()
        percent = min(100, round((completed / goal) * 100))
        self.progress.setValue(percent)
        self.progress.setFormat(f"{completed} of {goal} minutes completed ({percent}%)")
        count = self.task_table.rowCount()
        self.summary.setText(
            "No tasks planned yet — add one to get started!" if count == 0
            else f"{count} task(s) planned • {total} total minutes"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudyPlanner()
    window.show()
    sys.exit(app.exec())
