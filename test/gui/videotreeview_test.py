from PyQt4 import QtGui
from PyQt4 import QtCore
from collections import defaultdict
import unittest
from gui.videotreeview import VideoTreeModel
from modules.search import Movie


class TestVideoTreeModel(unittest.TestCase):

    def setUp(self):
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        self.main_window.show()

    def test_add_movie_to_tree_model(self):
        class CountingVideoTreeModel(VideoTreeModel):
            def __init__(self, parent=None):
                self.calls = []
                super().__init__(parent)

            def data(self, index, role):
                self.calls.append(role)
                super().data(index, role)

        model = CountingVideoTreeModel()

        self.main_window.tree_view = QtGui.QTreeView(self.main_window)
        self.main_window.tree_view.setModel(model)
        self.main_window.setCentralWidget(self.main_window.tree_view)

        movieinfo = defaultdict(lambda: "test")
        movieinfo['subtitles'] = []
        movieinfo['TotalSubs'] = 0
        movieinfo['MovieID'] = {'Link': 'test', 'LinkImdb': 'test', 'MovieID': 1}
        movie = Movie(movieinfo)

        model.setMovies([movie])
        self.app.processEvents()

        self.assertIn(QtCore.Qt.ForegroundRole, model.calls, 'ForegroundRole not called')
        self.assertIn(QtCore.Qt.DecorationRole, model.calls, 'DecorationRole not called')
        self.assertIn(QtCore.Qt.FontRole, model.calls, 'FontRole not called')
        self.assertIn(QtCore.Qt.DisplayRole, model.calls, 'DisplayRole not called')
        self.assertIn(QtCore.Qt.SizeHintRole, model.calls, 'SizeHintRole not called')


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(600,400)

        movieinfo = defaultdict(lambda: "test")
        movieinfo['subtitles'] = []
        movieinfo['TotalSubs'] = 0
        movieinfo['MovieID'] = {'Link': 'test', 'LinkImdb': 'test', 'MovieID': 1}
        movie = Movie(movieinfo)

        self.treeview = QtGui.QTreeView(self)
        self.treeview.model = VideoTreeModel()
        self.treeview.model.setMovies([movie])
        self.treeview.setModel(self.treeview.model)
        self.treeview.setColumnWidth(0, 200)

        self.setCentralWidget(self.treeview)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


