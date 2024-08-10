from PIL import Image #library to access the image specifiactions

pix_count = 0

def is_fire_color(rgb): #setting the colour settings for particular pattern
    r, g, b = rgb
    return (180 <= r <= 255) and (60 <= g <= 140) and (0 <= b <= 60)


def check_continuous_fire_color(image_path, min_pixels=5):
    global pix_count, width
    img = Image.open(image_path)
    img = img.convert("RGB")
    
    width, height = img.size
    
    for y in range(height): #analysing the image
        continuous_count = 0 
        for x in range(width):
            current_rgb = img.getpixel((x, y))
            
            if is_fire_color(current_rgb):
                continuous_count += 1
                pix_count += 1 
                if continuous_count >= min_pixels:
                    return True
            else:
                continuous_count = 0 
    
    return False

image_path = "p8.jpg"
result = check_continuous_fire_color(image_path)


if result:  #conditional output statement
    print("Image suggests wildfire occurence")
    print("The percentage is {:.2f}% fired!".format((pix_count*1000)/width))
else:
    print("Least chances of wildfire")
    print("The percentage is {:.2f}% fired!".format((pix_count*1000)/width))