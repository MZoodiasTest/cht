    def find(self, icestone_img, threshold=0.5, debug_mode=None):
        
        
        icestone_img = cv.cvtColor(icestone_img, cv.COLOR_BGR2GRAY)
        
        result = cv.matchTemplate(icestone_img, self.needle_img, self.method)

    
    
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]

            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)


        points = []
        if len(rectangles):
    

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS


            for (x, y, w, h) in rectangles:

      
                center_x = x + int(w/2)
                center_y = y + int(h/2)

                points.append((center_x, center_y))

                if debug_mode == 'rectangles':

                    top_left = (x, y)
                    bottom_right = (x + w, y + h)

                    cv.rectangle(icestone_img, top_left, bottom_right, color=line_color, 
                                lineType=line_type, thickness=2)
                elif debug_mode == 'points':

                    cv.drawMarker(icestone_img, (center_x, center_y), 
                                color=marker_color, markerType=marker_type, 
                                markerSize=40, thickness=2)

        if debug_mode:
            cv.imshow('Matches', icestone_img)

        return points