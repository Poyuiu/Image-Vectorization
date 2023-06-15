import aspose.words as aw


def svg2png(fileName):
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    shape = builder.insert_image(fileName)
    pageSetup = builder.page_setup
    pageSetup.page_width = shape.width
    pageSetup.page_height = shape.height
    pageSetup.top_margin = 0
    pageSetup.left_margin = 0
    pageSetup.bottom_margin = 0
    pageSetup.right_margin = 0
    doc.save("result.png")
