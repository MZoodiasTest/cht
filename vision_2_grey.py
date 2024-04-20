    def find(self, icestone_img, threshold=0.5, debug_mode=None):
        # Convert the image to grayscale
        icestone_img = cv.cvtColor(icestone_img, cv.COLOR_BGR2GRAY)

        # Resize the needle image to the same size as the template
        needle_resized = cv.resize(self.needle_img, (self.needle_w, self.needle_h))

        # Convert the needle image to grayscale
        needle_resized = cv.cvtColor(needle_resized, cv.COLOR_BGR2GRAY)

        # Compute the correlation between the needle image and the input image
        result = cv.matchTemplate(icestone_img, needle_resized, self.method)

        # Find the locations of the matches
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # Group the rectangles that are close to each other
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        # Compute the center of each detected object
        points = []
        if len(rectangles):
            for (x, y, w, h) in rectangles:
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                points.append((center_x, center_y))

        if debug_mode:
            # Draw rectangles around the detected objects
            if debug_mode == 'rectangles':
                for (x, y, w, h) in rectangles:
                    cv.rectangle(icestone_img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Draw crosses at the center of each detected object
            elif debug_mode == 'points':
                for point in points:
                    cv.drawMarker(icestone_img, point, (0, 255, 0), cv.MARKER_CROSS, 40, 2)

            # Display the results
            cv.imshow('Matches', icestone_img)

        return points