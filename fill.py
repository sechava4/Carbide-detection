import numpy as np
import cv2

if __name__ == '__main__':


    img = cv2.imread('8.jpg', True)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_grey = cv2.resize(img_grey, (1000, 1000))
    img_grey = img_grey[300:700,300:700]
    blur = cv2.GaussianBlur(img_grey, (3, 3), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    h, w = img_grey.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    seed_pt = None
    fixed_range = False

    #Pixeles juntos
    connectivity = 8

    def update(dummy=None):
        if seed_pt is None:
            cv2.imshow('floodfill', blur)
            return
        flooded = blur.copy()
        lo = cv2.getTrackbarPos('lo', 'floodfill')
        hi = cv2.getTrackbarPos('hi', 'floodfill')

        flags = connectivity
        if fixed_range:
            flags |= cv2.FLOODFILL_FIXED_RANGE
        cv2.floodFill(flooded, None, None, (255, 0, 255), (lo,)*3, (hi,)*3, flags)
        indices = np.where(flooded == [255])

        frac = 1-(np.divide(len(indices[0]), int((h*w))))
        percent = np.multiply((float(frac)), 100)
        print('Frac: ' + str(percent) + '%')
        #cv2.floodFill(flooded, mask, seed_pt, (255, 255, 255), (lo,) * 3, (hi,) * 3, 4 | ( 255 << 8 ))
        cv2.imshow('floodfill', flooded)
        #fcv2.imshow('blur', blur)

    def onmouse(event, x, y, flags, param):
        global seed_pt
        if flags & cv2.EVENT_FLAG_LBUTTON:
            seed_pt = x, y
            update()

    update()
    cv2.setMouseCallback('floodfill', onmouse)
    cv2.createTrackbar('lo', 'floodfill', 20, 255, update)
    cv2.createTrackbar('hi', 'floodfill', 20, 255, update)
    cv2.setTrackbarPos('lo', 'floodfill', 1)
    cv2.setTrackbarPos('hi', 'floodfill', 1)

    while True:
        ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break
        if ch == ord('f'):
            fixed_range = not fixed_range
            print ('using %s range' % ('floating', 'fixed')[fixed_range])
            update()
        if ch == ord('c'):
            connectivity = 12 - connectivity
            print
            'connectivity =', connectivity
        update()
        if ch == ord('q'):
            update()


cv2.destroyAllWindows()