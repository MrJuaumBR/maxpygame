import os

def count_lines(file_path:str, whitelist:list[str,],blacklist_folder:list[str,]=[]) -> tuple[int, int]:
    lines = 0
    files = 0
    for dir in os.listdir(file_path):
        
        if os.path.isfile(os.path.join(file_path, dir)):
            if str(dir).split('.')[-1] in whitelist:
                with open(os.path.join(file_path, dir), 'rb') as f:
                    lines += len(f.readlines())
                    files += 1
        elif os.path.isdir(os.path.join(file_path, dir)):
            if not (dir in blacklist_folder):
                l,f = count_lines(os.path.join(file_path, dir), whitelist,blacklist_folder)
                lines += l
                files += f + 1
    return lines, files

Whitelist:list[str,] = ['py','txt','md','json','toml','cfg']
BlacklistFolder:list[str,] = ['venv','node_modules','.git','.github','dist','build','__pycache__','maxpygame.egg-info']
Lines, Files = count_lines('./',Whitelist,BlacklistFolder)


print(f"""
      Line Counter by MrJuaum
      -----------------------
      Lines: {Lines}
      Files: {Files}
      
      Whitelist ({len(Whitelist)}): {Whitelist}
      Blacklist Folder ({len(BlacklistFolder)}): {BlacklistFolder}
      """)