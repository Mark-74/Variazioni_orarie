import discord, requests, datetime, os, camelot, asyncio

days = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']
month_names = {
    1: "gennaio", 2: "febbraio", 3: "marzo", 4: "aprile", 5: "maggio", 6: "giugno",
    7: "luglio", 8: "agosto", 9: "settembre", 10: "ottobre", 11: "novembre", 12: "dicembre"
}

class server:
    @staticmethod
    def get_url(day_of_week: str, day_number: int, month: str) -> str:
        return f"https://www.ispascalcomandini.it/wp-content/uploads/2017/09/variazioni-orarie-{day_of_week}-{day_number}-{month}-1.pdf"
    
    @staticmethod 
    def make_output_row(class_identifier: str, hour: int | None, absent_professor: str, substitute: str, note: str) -> object:
        return {
            'class':class_identifier,
            'hour': hour,
            'absent_professor': absent_professor,
            'substitute': substitute,
            'note': note
        }
        
    def __init__(self, guild: discord.Guild, channel: discord.channel, class_identifier: str) -> None:
        self.guild = guild
        self.channel = channel
        self.class_identifier = class_identifier
    
    async def update(self): #TODO: add txt of previous variations to update only the new ones
        current_date = datetime.datetime.now()
        day_of_week = days[(current_date.weekday() + 1) % 7]
        day_number = current_date.day
        month = month_names[current_date.month]
        
        if day_of_week == days[6]: return
        
        pdf_path = f'./{month}-{day_number}.pdf'
        
        if not os.path.exists(pdf_path):
            
            response = await requests.get(self.get_url(day_of_week=day_of_week, day_number=day_number, month=month))
            
            with open(pdf_path, 'wb') as file:
                file.write(response.content)
                
        output = []

        tables = camelot.read_pdf(pdf_path)
        for table in tables:
            rows = table.df.values.tolist()
            rows.pop(0) #removing how to read the data in the spreadsheet
            
            data = [row[0].split("\n") for row in rows]
            
            for row in data:
                if row[0] == self.class_identifier:
                    try:
                        output.append(self.make_output_row(self.class_identifier, int(row[1]), row[2], row[3], row[-2]))
                    except: pass
        
        for variation in output:
            #if variation['absent_professor'] == '-': variation['absent_professor'] = 'Nessun sostituto'
            embed = embed = discord.Embed(title=f"{variation['class']} - Variazione", color=0x1dcf4c)
            embed.add_field(name=f"{variation['hour']} ora - Docente assente: ", value=f"{variation['absent_professor']} -> {variation['substitute']}", inline=False)
            embed.add_field(name="Note: ", value=variation['note'], inline=False)
            embed.set_footer(text="---------------------------------------------------------------------------------")
            
            await self.channel.send(embed=embed)
