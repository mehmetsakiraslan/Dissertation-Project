def get_cups(detections):
    cups = []
    for detection in detections:
        if detection.ClassID == 47:
            cups.append(detection)
    return cups

def get_center_cup(cups):
    cup_centers = [cup.Center for cup in cups]
    center = (1280/2, 720/2)
    distances = [dist(cup_center, center) for cup_center in cup_centers]
    min_idx = distances.index(min(distances))
    return cups[min_idx]
    
def dist(t1, t2):
    return ((t1[0] - t2[0])**2 + (t1[1] - t2[1])**2)**0.5 
