import time
import random
import DMXEnttecPro
import DMXEnttecPro.utils

class Universe:
    def __init__(self, universe_number, channels, name) -> None:
        self.universe_number = universe_number
        self.channels = [0] * channels
        self.name = name
        self.interface = None

        Universe_handler.Universes.append(self)

    def __repr__(self) -> str:
        return f"repr-name: {self.name}"

    def __str__(self) -> str:
        return f"str-name: {self.name}"

    def get_channel_amount(self):
        return len(self.channels)
    
    def get_universe_number(self):
        return self.universe_number
    
    def set_channel(self, channel, value):
        channel = channel-1
        self.channels[channel] = value

    def set_interface(self, interface):
        self.interface = interface

    def copy_to_interface(self):
        print(self.name)
        print("REACHED")
        # # print(self.interface.channel)
        # self.channels[0] = 199
        # self.channels[1] = 200
        # self.channels[2] = 201
        Universe_handler.print_universe(1)
        for index, i in enumerate(self.channels):
            # print(index)
            # print("value " + str(i))
            # print(f"Uni: {self.channels[i]}")
            # print(f"Int: {self.interface.channel[i]}")
            self.interface.channel[index] = i

        # #test
        # self.interface.channel[0] = 255
        # self.interface.channel[1] = 255
        # self.interface.channel[2] = 255
        print("Should have copied all channels from Uni to Interface")
    
class Universe_handler:
    Universes = []

    @classmethod
    def create_universe(cls, universe_number, channels, name) -> bool:

        if not (type(universe_number) == int):
            print(f"{universe_number} is not a number.")
            return False
        
        if not (0 < universe_number):
            print(f"{universe_number} is not higher then 1.")
            return False
        
        for universe in Universe_handler.Universes:
            if(universe_number == universe.get_universe_number()):
                print(f"{universe_number} is already in use.")
                return False

        if not (type(channels) == int):
            print(f"Channel with value '{channels}' is not a number.")
            return False
        
        if not (0 <= channels and channels <= 512):
            print(f"Amount of channels of {channels} is not between 0 and 2048")
            return False
        
        if not (type(name) == str):
            print(f"'{name}' is not a valid name for an universe.")
            return False
        
        Universe(universe_number, channels, name)

        print(f"Universe created with name '{name}', #{universe_number} and {channels} channels!")
        return True


    @classmethod
    def get_universe(cls, universe_number):
        for universe in Universe_handler.Universes:
            if(universe_number == universe.get_universe_number()):
                return universe
        print(f"No universe with # {universe_number}")
        return None    

    @classmethod
    def print_universes_info(cls):
        print("#" * 40)
        for universe in cls.Universes:
            print(f"Universe #{universe.universe_number}, Channels #{universe.get_channel_amount()}, name: {universe.name}")

    @classmethod
    def set_channel(cls, universe, channel, value):
        u = cls.get_universe(universe)
        if not (type(value) == int):
            print("Not a fucking number bro!")
            return
        if (value < 0):
            u.set_channel(channel, 0)
            print("Lower then 0")
            return
        if (value > 255):
            print("higher then 255")
            u.set_channel(channel, 255)
            return
        
        # print("GOOD BOI")
        u.set_channel(channel, value)

    @classmethod
    def print_universe(cls, universe_number):
        u = Universe_handler.get_universe(universe_number)
        print(u)

        print(u.get_universe_number())

        output = f"UNI{universe_number:02} "

        for x in range(1, 33):
            output += f"(+{x:02}) "

        output += "\n(000) "
        
        for channel, value in enumerate(u.channels):
            output += f"[{value:03}] "
            if((channel + 1) % 32 == 0):
                output += "\n"
                output += f"({(channel+1):03}) "
            
        print(output)

    @classmethod
    def copy_channel_values_to_interfaces(cls):
        for uni in cls.Universes:
            if not uni.interface == None:
                print(f"Copying for {uni}")
                uni.copy_to_interface()

class Main:
    
    @classmethod
    def main(cls):
        # Timing performance
        start_time = time.time()
        handler = Universe_handler()
        handler.create_universe(1, 501, "Universe 1")
        handler.create_universe(2, 502, "Universe 2")
        handler.create_universe(3, 503, "Universe 3")
        handler.create_universe(4, 504, "Universe 4")
        handler.create_universe(5, 512, "Universe 5")
        handler.print_universes_info()

        # handler.set_channel(5, 1, 124)

        # for x in range(1000):
        #     chan = random.randint(1, 512)
        #     val = random.randint(0, 255)
        #     handler.set_channel(5, chan, val)

        # handler.print_universe(5)

        handler.set_channel(1, 1, 0)
        handler.set_channel(1, 2, 255)
        handler.set_channel(1, 3, 0)

        print("#" * 40)

        Interface_handler.check_interfaces()
        Interface_handler.check_interfaces()

        Dmx_interface.print_interfaces_serial()

        Universe_handler.get_universe(1).interface = Enttec_pro_interface.get_interface_by_serial('EN397335A')
        print("Connected Uni 1 and interface 'EN397335A'")
        Universe_handler.get_universe(2).interface = Enttec_pro_interface.get_interface_by_serial('EN132491A')
        print("Connected Uni 2 and interface 'EN132491A'")
        print("I hope")

        # Copy all the values of an Universe.channels to Interface.channels

        Universe_handler.print_universe(1)

        Universe_handler.copy_channel_values_to_interfaces()

        x = Enttec_pro_interface.get_interface_by_serial('EN397335A').channel
        print(x)

        Interface_handler.copy_channels_values_to_enttec()

        while(True):
            
            handler.set_channel(1, 1, random.randint(0, 255))
            handler.set_channel(1, 2, random.randint(0, 255))
            handler.set_channel(1, 3, random.randint(0, 255))
            
            
            Universe_handler.copy_channel_values_to_interfaces()
            Interface_handler.copy_channels_values_to_enttec()




        print("--- %s seconds ---" % (time.time() - start_time))



class Dmx_interface:
    interfaces = []
    hardware_connected = False

    @classmethod
    def print_interfaces_serial(cls):
        for i in cls.interfaces:
            print(f"Interface {i.serial}")

    def __repr__(self) -> str:
        return "interface X"
    
    def __str__(self) -> str:
        return "str interface X"


class Enttec_pro_interface(Dmx_interface):
    
    def __init__(self, serial, name) -> None:
        print("reached")
        super().__init__()
        self.serial = serial
        self.name = name
        self.port = DMXEnttecPro.utils.get_port_by_serial_number(str(serial))
        self.dmx = DMXEnttecPro.Controller(self.port, auto_submit=True)
        self.channel = [0] * 512
        Dmx_interface.interfaces.append(self)

    @classmethod
    def get_interface_by_serial(cls, serial):
        for i in Dmx_interface.interfaces:
            if str(i.serial) == serial:
                return i
        print("No interface found with that serial")
        return None
    
    def send_channel_package(self):
        for index,value in enumerate(self.channel):
            self.dmx.set_channel(index+1, value)

    

    

    
    

class Interface_handler:


    # 1. Check for connected interface
    # > new? -> add & mark connected
    # > old? -> mark connected
    # 
    @classmethod
    def check_interfaces(cls):
        connected = []
        print("checking connected interfaces")
        for port in DMXEnttecPro.utils.slp.comports():
            connected.append(port.serial_number)
        
        print(connected)

        # Add interfaces that didn't originally exist
        for c in connected:
            found = False
            print(c)
            for i in Dmx_interface.interfaces:
                if str(c) == str(i.serial):
                    print("exists!")
                    found = True
                    i.hardware_connected = True
                
                # Dus als connected interface nog niet bestond (en dus toegevoegd moet worden)
            if(found == False):
                print("new interface found!")
                new_name = f"new interface '{c}'"
                Enttec_pro_interface(c, new_name)

    @classmethod
    def copy_channels_values_to_enttec(cls):
        print("Begin sending")
        for i in Dmx_interface.interfaces:
            i.send_channel_package()
        print("Seond all packages!")

    # @classmethod
    # def print_universe(cls, interface):
    #     i = Dmx_interface.
    #     print(u)

    #     print(u.get_universe_number())

    #     output = f"UNI{universe_number:02} "

    #     for x in range(1, 33):
    #         output += f"(+{x:02}) "

    #     output += "\n(000) "
        
    #     for channel, value in enumerate(u.channels):
    #         output += f"[{value:03}] "
    #         if((channel + 1) % 32 == 0):
    #             output += "\n"
    #             output += f"({(channel+1):03}) "
            
    #     print(output)


Main.main()
