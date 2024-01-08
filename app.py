from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from Adafruit_IO import Client
import os

ADAFRUIT_IO_USERNAME = 'chathurazju'
ADAFRUIT_IO_KEY = 'aio_fTGR25ihhqnx65rtc2aTOdaL8ODV'
FEED_NAME = 'power'  # Replace with your feed name

# Check for proxy settings from environment variables
proxies = {
    'http': os.environ.get('HTTP_PROXY'),
    'https': os.environ.get('HTTPS_PROXY')
}

# Create an instance of the Adafruit IO REST client with proxy settings
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY, proxies=proxies)

class PowerApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')

        # Create the image for displaying the animation
        self.animation = Image()
        self.root.add_widget(self.animation)

        # Schedule the update of animations
        self.update_animation()
        return self.root

    def get_power_consumption(self):
        try:
            data = aio.receive(FEED_NAME)
            print("Received data:", data)  # Print received data for debugging
            if data is not None:
                value = float(data.value)
                processed_value = int(round(value))  # Process value to an integer without decimals
                return processed_value
            else:
                return None
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def update_animation(self, *args):
        processed_value = self.get_power_consumption()

        if processed_value is not None:
            # Update image source based on processed value
            if processed_value < 30:
                self.animation.source = '1.png'
            elif 30 <= processed_value < 70:
                self.animation.source = '2.png'
            else:
                self.animation.source = '3.png'

        # Schedule the next update
        from kivy.clock import Clock
        Clock.schedule_once(self.update_animation, 5)

if __name__ == '__main__':
    PowerApp().run()
