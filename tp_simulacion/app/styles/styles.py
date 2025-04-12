style = """
QWidget {
background-color: #F1F3F9;
font-family: 'Segoe UI', 'Arial', sans-serif;
font-size: 18px;
color: #212529;
}

QLabel {
    color: #495057;
    margin-top: 6px;
    font-weight: 500;
    font-size: 19px;
}

QLineEdit, QComboBox, QTextEdit {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 18px;
    selection-background-color: #74b9ff;
}

QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
    border: 1px solid #5c9ded;
    outline: none;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    selection-background-color: #5c9ded;
    selection-color: white;
    font-size: 18px;
}

QPushButton {
    background-color: #5c9ded;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 14px 24px;
    font-weight: bold;
    font-size: 19px;
}

QPushButton:hover {
    background-color: #468ce0;
}

QPushButton:pressed {
    background-color: #3a76c5;
}

QCheckBox {
    padding: 8px;
    font-size: 18px;
}

QTextEdit {
    border: 1px solid #aaa;
    background-color: #ffffff;
    border-radius: 10px;
    font-size: 18px;
}

QScrollBar:vertical {
    border: none;
    background: #e9ecef;
    width: 14px;
    margin: 2px 0 2px 0;
    border-radius: 7px;
}

QScrollBar::handle:vertical {
    background: #5c9ded;
    min-height: 30px;
    border-radius: 7px;
}

QScrollBar::handle:vertical:hover {
    background: #468ce0;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}


QScrollBar:horizontal {
    border: none;
    background: #e9ecef;
    height: 14px;
    margin: 0 2px 0 2px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background: #5c9ded;
    min-width: 30px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal:hover {
    background: #468ce0;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

QComboBox {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 18px;
    color: #212529;
}

QComboBox:hover {
    border: 1px solid #5c9ded;
}

QComboBox:focus {
    border: 1px solid #5c9ded;
    outline: none;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left: 1px solid #ced4da;
    background-color: #e9ecef;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
}

QComboBox::down-arrow {
    image: url(tp_simulacion/assets/icons/arrow.svg); 
    width: 14px;
    height: 14px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    selection-background-color: #5c9ded;
    selection-color: white;
    border-radius: 8px;
    font-size: 18px;
}

QComboBox QScrollBar:vertical {
    border: none;
    background: #e9ecef;
    width: 14px;
    margin: 2px 0 2px 0;
    border-radius: 7px;
}

QComboBox QScrollBar::handle:vertical {
    background: #5c9ded;
    min-height: 30px;
    border-radius: 7px;
}

QComboBox QScrollBar::handle:vertical:hover {
    background: #468ce0;
}

QComboBox QScrollBar::add-line:vertical,
QComboBox QScrollBar::sub-line:vertical {
    height: 0px;
}

QComboBox QScrollBar::add-page:vertical,
QComboBox QScrollBar::sub-page:vertical {
    background: none;
}

QCheckBox {
    spacing: 10px;
    font-size: 18px;
    padding: 6px;
    color: #212529;
}

QCheckBox::indicator {
    width: 22px;
    height: 22px;
    border: 2px solid #ced4da;
    border-radius: 4px;
    background-color: #fff;
}

QCheckBox::indicator:hover {
    border: 2px solid #5c9ded;
}

QCheckBox::indicator:checked {
    background-color: #5c9ded;
    border: 2px solid #5c9ded;
    image: url(tp_simulacion/assets/icons/checkbox.svg); 
}

QCheckBox::indicator:unchecked {
    background-color: #ffffff;
}


"""