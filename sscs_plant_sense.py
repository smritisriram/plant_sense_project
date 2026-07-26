import serial
import time


PORT = "/dev/cu.usbserial-A5069RR4"

arduino = serial.Serial(PORT, 9600)

time.sleep(2)

print("🌱 PlantSense Connected\n")


# ==========================
# Plant Database
# ==========================

plants = {

    "Pothos": {
        "temp": (18,30),
        "humidity": (40,70),
        "light": (300,800)
    },

    "Snake Plant": {
        "temp": (15,30),
        "humidity": (30,70),
        "light": (100,600)
    },

    "ZZ Plant": {
        "temp": (15,30),
        "humidity": (40,60),
        "light": (100,600)
    },

    "Peace Lily": {
        "temp": (18,27),
        "humidity": (50,70),
        "light": (200,700)
    },

    "Spider Plant": {
        "temp": (15,25),
        "humidity": (40,80),
        "light": (300,700)
    },

    "Monstera": {
        "temp": (18,30),
        "humidity": (50,80),
        "light": (400,800)
    },

    "African Violet": {
        "temp": (18,24),
        "humidity": (50,60),
        "light": (500,900)
    },

    "Orchid": {
        "temp": (18,29),
        "humidity": (50,70),
        "light": (500,900)
    },

    "Anthurium": {
        "temp": (16,32),
        "humidity": (60,80),
        "light": (600,1000)
    },

    "Kalanchoe": {
        "temp": (15,27),
        "humidity": (30,50),
        "light": (700,1023)
    },

    "Aloe Vera": {
        "temp": (15,30),
        "humidity": (10,40),
        "light": (700,1023)
    },

    "Cactus": {
        "temp": (20,35),
        "humidity": (10,40),
        "light": (800,1023)
    },

    "Basil": {
        "temp": (18,30),
        "humidity": (40,70),
        "light": (700,1023),
        "importance":"high light"
    },

    "Rubber Plant": {
        "temp": (18,30),
        "humidity": (40,60),
        "light": (400,800)
    },

    "Cast Iron Plant": {
        "temp": (15,28),
        "humidity": (40,70),
        "light": (100,400)
    }

}



# ==========================
# Matching System
# ==========================

def calculate_match(plant, temp, humidity, light):

    data = plants[plant]

    score = 0


    # -----------------------
    # Temperature (40%)
    # -----------------------

    temp_min, temp_max = data["temp"]

    ideal_temp = (temp_min + temp_max) / 2

    temp_difference = abs(temp - ideal_temp)

    temp_score = max(
        0,
        40 - (temp_difference * 3)
    )

    score += temp_score



    # -----------------------
    # Humidity (40%)
    # -----------------------

    hum_min, hum_max = data["humidity"]

    ideal_hum = (hum_min + hum_max) / 2

    humidity_difference = abs(
        humidity - ideal_hum
    )

    humidity_score = max(
        0,
        40 - humidity_difference
    )

    score += humidity_score



    # -----------------------
    # Light (20%)
    # -----------------------

    light_min, light_max = data["light"]

    ideal_light = (light_min + light_max) / 2

    light_difference = abs(
        light - ideal_light
    )


    light_score = max(
        0,
        20 - (light_difference / 30)
    )

    score += light_score


    return round(score)




# ==========================
# Main Loop
# ==========================


while True:

    try:

        line = arduino.readline().decode("utf-8").strip()


        if line:

            temp, humidity, light = line.split(",")

            temp = float(temp)
            humidity = float(humidity)
            light = int(light)



            results = {}


            for plant in plants:

                results[plant] = calculate_match(
                    plant,
                    temp,
                    humidity,
                    light
                )



            ranked = sorted(
                results.items(),
                key=lambda x:x[1],
                reverse=True
            )


            bestPlant = ranked[0][0]
            bestScore = ranked[0][1]



            print("----------------------")
            print("Temperature:",temp,"°C")
            print("Humidity:",humidity,"%")
            print("Light:",light)

            print("\nTop Matches:")


            for plant,score in ranked[:3]:
                print(
                    plant,
                    "-",
                    score,
                    "%"
                )


            print(
                "\nSending:",
                bestPlant,
                bestScore,
                "%"
            )



            # Send best result to Arduino

            arduino.write(
                (bestPlant + "," + str(bestScore) + "\n").encode()
            )


    except Exception as e:

        print("Error:",e)
