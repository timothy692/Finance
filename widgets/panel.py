from PyQt6.QtGui import QFont, QIcon, QColor, QPixmap, QPainter
from PyQt6.QtCore import Qt as qt
from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QSizePolicy, QVBoxLayout

from .dynamicWidget import DynamicWidget


class PanelWidget(DynamicWidget, QFrame):
    def __init__(self, title: str, initial_values: dict):
        DynamicWidget.__init__(self)
        QFrame.__init__(self)

        self._diff = 0
        self._amount = 0

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setObjectName('frame')

        self.setStyleSheet(
            '''
            QFrame#frame {
                border: 2px solid #7D7BFF;
                border-radius: 10px;
                background-color: #F8F8FF;
                padding: 8px;
            }
                           
            QLabel {
                background-color: #F8F8FF;
            }
            '''
        )

        self.setMinimumWidth(380)
        self.setFixedHeight(130)

        self._init_layout(title)

        self.update(initial_values)  

    def update(self, values: dict) -> None:
        self._diff += values['difference']
        self._amount += values['amount']

        self._update_indicator(self._diff)
        self._update_value_label(self._amount)

    def _update_indicator(self, difference: int):
        pixmap_asset = 'assets/icons/uptrend.png' if difference > 0 else 'assets/icons/downtrend.png'
        icon_pixmap = QPixmap(pixmap_asset).scaled(22, 22, 
                                                           qt.AspectRatioMode.KeepAspectRatio, 
                                                           qt.TransformationMode.SmoothTransformation)
        self._indicator_icon.setPixmap(icon_pixmap)
        
        self._indicator_label.setText(f'{difference}% vs last month')

    def _update_value_label(self, amount: str):
        self._value_label.setText('${:,.2f}'.format(amount))  

    def _init_layout(self, title: str) -> None:
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        label_layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont('Inter Regular', 14))
        title_label.setStyleSheet(
            'color: #545454;'
        )
        
        # Value label indicating the amount
        self._value_label = QLabel()
        self._value_label.setFont(QFont('Inter Regular', 19))
        self._value_label.setStyleSheet(
            'color: black;'
        )

        indicator_layout = QHBoxLayout()
        indicator_layout.setContentsMargins(0, 0, 0, 0)
        indicator_layout.setSpacing(5) 

        # Indicator icon indicating downtrend or uptrend
        self._indicator_icon = QLabel()

        # Indicator label indicating % vs last month
        self._indicator_label = QLabel()
        self._indicator_label.setFont(QFont('Inter Regular', 12))
        self._indicator_label.setStyleSheet('color: #545454;')

        indicator_layout.addWidget(self._indicator_icon)
        indicator_layout.addWidget(self._indicator_label)

        indicator_widget = QFrame()
        indicator_widget.setStyleSheet('background-color: transparent;')
        indicator_widget.setLayout(indicator_layout)

        label_layout.addWidget(title_label, alignment=qt.AlignmentFlag.AlignLeft)
        label_layout.addWidget(self._value_label, alignment=qt.AlignmentFlag.AlignLeft)
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