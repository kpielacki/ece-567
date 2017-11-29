import dash_html_components as html
from geopy.point import Point
from geopy.distance import vincenty


GOOD_GLYPH = html.Span(className='glyphicon glyphicon-ok',
                       style={'color': 'green'})
WARN_GLYPH = html.Span(className='glyphicon glyphicon-warning-sign',
                       style={'color': 'orange'})
BAD_GLYPH = html.Span(className='glyphicon glyphicon-remove',
                       style={'color': 'red'})


def vicinity_rate(src_points, comp_points, mile_thresh):
    """Returns rate of time spent within mile threshold for series of points.

    :src_lat (float): Source latitude of source comparison.
    :src_points (list of 2 entry float tuples): List of source points to 
                                                compare within comp_points.
    :comp_points (list of 2 entry float tuples): List of comparison points to 
                                                 compare within source_points.
    :mile_thresh (float): Mile threshold points must be within to increase rate.

    :returns (float): Vicinity rate of points within mile_thresh to source.
    """
    cnt = 0
    for comp_lat, comp_lon in comp_points:
        comp_point = Point(comp_lat, comp_lon)
        for src_lat, src_lon in src_points:
            src_point = Point(src_lat, src_lon)
            miles = vincenty(src_point, comp_point).miles
            if miles <= mile_thresh:
                cnt += 1
                break

    return float(cnt) / len(comp_points)


if __name__ == '__main__':
    points_1 = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
    points_2 = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    test_rate = vicinity_rate(points_1, points_2, 5)
    print test_rate
