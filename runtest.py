modules = [
    'testFeedvalidator',
    'testUri',
    'testXmlEncoding',
    'testXmlEncodingDecode',
    'testMediaTypes',
    'testHowtoNs',
    'validtest',
    'mkmsgs',
]

if __name__ == '__main__':
    import os, sys, unittest

    srcdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'src')
    testdir = os.path.join(srcdir,'tests')
    xdocsdir = os.path.join(os.path.dirname(srcdir),'docs-xml')
    sys.path.insert(0,srcdir)
    sys.path.insert(0,testdir)
    sys.path.insert(0,xdocsdir)

    suite = unittest.TestSuite()
    for module in modules:
        suite.addTest(__import__(module).buildTestSuite())
    unittest.TextTestRunner().run(suite)
