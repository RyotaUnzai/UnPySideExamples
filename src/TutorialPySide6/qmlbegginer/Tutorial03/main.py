import sys

from PySide6 import QtGui, QtQml

qml = """
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    width: 320
    height: 240
    visible: true
    title: "Hello World"

    readonly property list<string> texts:[
        "Bonjour le monde", "Ciao mondo", "Hallo Welt", "Hallo Wereld", "Hello World"
    ]

    function setText() {
        var i = Math.round(Math.random() * 3)
        text.text = texts[i]
    }

    ColumnLayout {
        anchors.fill:  parent

        Text {
            id: text
            text: "Hello World"
            Layout.alignment: Qt.AlignHCenter
        }
        Button {
            text: "Click me"
            Layout.alignment: Qt.AlignHCenter
            onClicked: setText()
        }
    }
}

"""

if __name__ == "__main__":
    app = QtGui.QGuiApplication(sys.argv)
    engine = QtQml.QQmlApplicationEngine()
    engine.loadData(qml.encode("utf-8"))
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)
