from svgpathtools import svg2paths, Line, CubicBezier
import numpy as np

def calculate_mse(svg_file1, svg_file2):
    paths1, _ = svg2paths(svg_file1)
    paths2, _ = svg2paths(svg_file2)

    if len(paths1) != len(paths2):
        raise ValueError("Number of paths in SVG files must be the same.")

    squared_diff_sum = 0
    total_elements = 0

    for path1, path2 in zip(paths1, paths2):
        elements1 = path1._segments
        elements2 = path2._segments

        if len(elements1) != len(elements2):
            raise ValueError("Number of elements in paths must be the same.")
        for elem1, elem2 in zip(elements1, elements2):
            if isinstance(elem1, Line) and isinstance(elem2, Line):
                # 計算直線起點和終點的差異
                diff = np.abs(elem1.start - elem2.start) + np.abs(elem1.end - elem2.end)
                squared_diff = np.square(diff)
                squared_diff_sum += np.sum(squared_diff)
                total_elements += 1
                
            elif isinstance(elem1, CubicBezier) and isinstance(elem2, CubicBezier):
                # 計算CubicBezier curve 控制點和採樣點之間的差異
                control_diff = np.abs(elem1.start - elem2.start) + np.abs(elem1.control1 - elem2.control1) + np.abs(
                    elem1.control2 - elem2.control2)
                squared_control_diff = np.square(control_diff)
                squared_diff_sum += np.sum(squared_control_diff)
                total_elements += 1
                

                num_samples = 10  # 採樣點數量
                for t in np.linspace(0, 1, num_samples):
                    point_on_curve1 = elem1.point(t)
                    point_on_curve2 = elem2.point(t)
                    point_diff = np.abs(point_on_curve1 - point_on_curve2)
                    squared_point_diff = np.square(point_diff)
                    squared_diff_sum += np.sum(squared_point_diff)
                    total_elements += 1
    
    mse = squared_diff_sum / total_elements

    return mse



svg_file1 = "ground_truth.svg"
svg_file2 = "your_file.svg"

mse = calculate_mse(svg_file1, svg_file2)
print("MSE:", mse)