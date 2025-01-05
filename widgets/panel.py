from PyQt6.QtCore import QRectF
from PyQt6.QtCore import Qt as qt
from PyQt6.QtGui import QColor, QFont, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QSizePolicy,
                             QVBoxLayout)


class PanelWidget(QFrame):
    def __init__(self, title: str, value: float, diff: int):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setObjectName('frame')

        self.setStyleSheet("""
            QFrame#frame {
                border: 2px solid #7D7BFF;
                border-radius: 10px;
                background-color: #F8F8FF;
                padding: 8px;
            }
                           
            QLabel {
                background-color: #F8F8FF;
            }
        """)

        self.setMinimumWidth(380)
        self.setFixedHeight(130)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        label_layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont('Inter Regular', 14))
        title_label.setStyleSheet(
            'color: #545454;'
        )
        
        value_label = QLabel('${:,.2f}'.format(value))
        value_label.setFont(QFont('Inter Regular', 19))
        value_label.setStyleSheet(
            'color: black;'
        )

        indicator_layout = QHBoxLayout()
        indicator_layout.setContentsMargins(0, 0, 0, 0)
        indicator_layout.setSpacing(10) 

        icon_label = QLabel()

        pixmap_asset = 'assets/icons/uptrend.png' if diff >= 0 else 'assets/icons/downtrend.png'
        icon_pixmap = QPixmap(pixmap_asset).scaled(22, 22, 
                                                           qt.AspectRatioMode.KeepAspectRatio, 
                                                           qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)

        indicator = QLabel(f'{diff}% vs last month')
        indicator.setFont(QFont('Inter Regular', 12))
        indicator.setStyleSheet('color: #545454;')

        indicator_layout.addWidget(icon_label)
        indicator_layout.addWidget(indicator)

        indicator_widget = QFrame()
        indicator_widget.setStyleSheet('background-color: transparent;')
        indicator_widget.setLayout(indicator_layout)

        label_layout.addWidget(title_label, alignment=qt.AlignmentFlag.AlignLeft)
        label_layout.addWidget(value_label, alignment=qt.AlignmentFlag.AlignLeft)
        label_layout.addWidget(indicator_widget, alignment=qt.AlignmentFlag.AlignLeft)

        main_layout.addLayout(label_layout)

        grid_frame = self._grid_frame()
        grid_frame.setFixedSize(100, 100)
        main_layout.addWidget(grid_frame, alignment=qt.AlignmentFlag.AlignRight)

        self.setLayout(main_layout)

    def _grid_frame(self) -> QFrame:
        class GridFrame(QFrame):
            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)

                rect = self.rect()
                width = rect.width()
                height = rect.height()

                grid_color = QColor(125, 123, 255, 100)
                painter.setPen(grid_color)

                vertical_spacing = width // 4
                horizontal_spacing = height // 4

                for i in range(-1, 2):
                    x = width // 2 + i * vertical_spacing
                    painter.drawLine(x, 0, x, height)

                for i in range(-1, 2):
                    y = height // 2 + i * horizontal_spacing
                    painter.drawLine(0, y, width, y)

                painter.end()

        grid_frame = GridFrame()    
        grid_frame.setFixedSize(100, 100)  # Adjust size as needed
        grid_frame.setStyleSheet("background: transparent;")
        return grid_frame