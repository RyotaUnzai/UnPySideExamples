from PySide6 import QtCore, QtGui, QtWidgets


class QAbstractProgressCircular(QtWidgets.QWidget):
    value_changed: QtCore.Signal = QtCore.Signal(int)

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self._value: int = 0
        self._enable_text: bool = True
        self._font_family: str = "Segoe UI"
        self._font_size: int = 12
        self._font: QtGui.QFont = QtGui.QFont(self._font_family, self._font_size)
        self._font.bold = True
        self._suffix: str = "%"
        self._progress_width: int = 10
        self._enable_background: bool = True
        self._is_rounded: bool = True
        self._minimum: int = 0
        self._maximum: int = 100
        self._font_color: str = "#0088FF"
        self._background_color: str = "#44475a"
        self._progress_color: str = "#0088FF"
        self._progress_color_type: str = "flat"
        self._progress_blur_color: QtGui.QColor = QtGui.QColor(0, 0, 0, 0)
        self._path: QtGui.QPainterPath = QtGui.QPainterPath()

        self.setAutoFillBackground(True)
        self.setMinimumSize(100, 100)

        self.value_changed.connect(self._value_changed_callback)
        self.palette().setColor(QtGui.QPalette.Window, QtGui.QColor("#00000000"))

    @property
    def rounded(self) -> bool:
        return self._is_rounded

    @rounded.setter
    def rounded(self, value: bool) -> None:
        self._is_rounded = value

    @QtCore.Slot(int)
    def _value_changed_callback(self, value: int) -> int:
        return value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value
        self.set_value(self._value)

    def set_value(self, value: int) -> None:
        self._value = value
        self.value_changed.emit(self.value)
        self.repaint()

    @property
    def minimum(self) -> int:
        return self._minimum

    @minimum.setter
    def minimum(self, value: int) -> None:
        self._minimum = value

    @property
    def maximum(self) -> int:
        return self._maximum

    @maximum.setter
    def maximum(self, value: int) -> None:
        self._maximum = value

    def set_range(self, minimum: int, maximum: int) -> None:
        self._minimum = minimum
        self._maximum = maximum

    @property
    def progress_blur_color(self) -> QtGui.QColor:
        return self._progress_blur_color

    @progress_blur_color.setter
    def progress_blur_color(self, value: QtGui.QColor) -> None:
        self._progress_blur_color = value

    @property
    def progress_color_type(self) -> str:
        return self._progress_color_type

    @progress_color_type.setter
    def progress_color_type(self, value: str) -> None:
        self._progress_color_type = value

    @property
    def enable_text(self) -> bool:
        return self._enable_text

    @enable_text.setter
    def enable_text(self, value: bool) -> None:
        self._enable_text = value

    @property
    def font_family(self) -> str:
        return self._font_family

    @font_family.setter
    def font_family(self, value: str) -> None:
        self._font_family = value

    @property
    def suffix(self) -> str:
        return self._suffix

    @suffix.setter
    def suffix(self, value: str) -> None:
        self._suffix = value

    @property
    def progress_width(self) -> int:
        return self._progress_width

    @progress_width.setter
    def progress_width(self, value: int) -> None:
        self._progress_width = value

    @property
    def enable_background(self) -> bool:
        return self._enable_background

    @enable_background.setter
    def enable_background(self, value: bool) -> None:
        self._enable_background = value

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, value: int) -> None:
        self._font_size = value

    @property
    def progress_color(self) -> str:
        return self._progress_color

    @progress_color.setter
    def progress_color(self, value: str) -> None:
        self._progress_color = value

    @property
    def font_color(self) -> str:
        return self._font_color

    @font_color.setter
    def font_color(self, value: str) -> None:
        self._font_color = value

    @property
    def background_color(self) -> str:
        return self._background_color

    @background_color.setter
    def background_color(self, value: str) -> None:
        self._background_color = value

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        out_length = min(self.width(), self.height())
        in_length = out_length - self._progress_width
        margin = self._progress_width / 2
        value = self._value * 360 / self._maximum
        painter = QtGui.QPainter(self)
        self._path = QtGui.QPainterPath()
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        if self._enable_background:
            self._create_empty_bar(
                painter, margin, margin, in_length, in_length, 0, 360 * 16
            )

        if self._enable_text:
            self._create_text(
                painter,
                0,
                0,
                in_length + self._font_size,
                self.height() - self._font_size / 3,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                f"{self._value}",
            )
        self._create_progress_bar(
            painter,
            out_length,
            margin,
            margin,
            in_length,
            in_length,
            -90 * 16,
            -value * 16,
        )

        painter.end()
        return super().paintEvent(event)

    def _create_progress_bar(
        self,
        painter: QtGui.QPainter,
        qreal: int,
        x: int,
        y: int,
        width: int,
        height: int,
        start_angle: int,
        span_angle: int,
    ) -> None:
        progress_color: QtGui.QRadialGradient | QtGui.QConicalGradient | QtGui.QColor
        if self._progress_color_type == "blur":
            progress_color = QtGui.QRadialGradient(qreal / 2, qreal / 2, qreal / 2)
            progress_color.setColorAt(
                1 - ((self._progress_width / qreal) * 2), self._progress_blur_color
            )
            progress_color.setColorAt(
                1 - (self._progress_width / qreal), self._progress_color
            )
            progress_color.setColorAt(1, self._progress_blur_color)

        elif self._progress_color_type == "gradation":
            progress_color = QtGui.QConicalGradient(
                QtCore.QPointF(qreal / 2, qreal / 2), 270
            )
            progress_color.setColorAt(0, self._progress_blur_color)
            progress_color.setColorAt(0.001, self._progress_color)
            progress_color.setColorAt(1, self._progress_blur_color)
        else:
            progress_color = QtGui.QColor(self._progress_color)
        pen = QtGui.QPen(
            progress_color, self._progress_width, QtCore.Qt.PenStyle.SolidLine
        )
        if self._is_rounded:
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        else:
            pen.setCapStyle(QtCore.Qt.PenCapStyle.FlatCap)

        painter.setPen(pen)
        painter.drawArc(x, x, width, height, start_angle, span_angle)

    def _create_text(
        self,
        painter: QtGui.QPainter,
        x: int,
        y: int,
        width: int,
        height: int,
        flags: int,
        text: str,
    ) -> None:
        painter.setFont(self._font)
        pen = QtGui.QPen(
            QtGui.QColor(self._font_color),
            self._progress_width,
            QtCore.Qt.SolidLine,
        )
        painter.setPen(pen)
        painter.drawText(x, y, width, height, flags, text)

    def _create_empty_bar(
        self,
        painter: QtGui.QPainter,
        x: int,
        y: int,
        width: int,
        height: int,
        start_angle: int,
        span_angle: int,
    ) -> None:
        pen = QtGui.QPen(
            QtGui.QColor(self._background_color),
            self._progress_width,
            QtCore.Qt.SolidLine,
        )
        painter.setPen(pen)
        painter.drawArc(x, y, width, height, start_angle, span_angle)
