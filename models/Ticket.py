import json

class Ticket:
    def __init__(self,titulo,motivation,ac,to,tags,cmd,repo):
        self.titulo = titulo
        self.motivation = motivation
        self.ac = ac
        self.to = to
        self.tags = tags
        self.cmd = cmd
        self.repo = repo
    def __str__(self):
        return f"""titulo:{self.titulo}
motivation:{self.motivation}
ac:{self.ac}
to:{self.to}
tags:{self.tags}
cmd:{self.cmd}
repo:{self.repo}"""

    @classmethod
    def load(cls, filepath):
        models=[]
        with open(filepath, 'r') as file:
            m = json.load(file)

        for model_data in m:
            titulo = model_data['titulo']
            motivation = model_data['motivation']
            ac = model_data['ac'] if 'ac' in model_data else ['Hay un screen en los comentarios que cumpla la motivation']
            to = model_data['to'] if 'to' in model_data else ''
            tags = model_data['tags'] if 'tags' in model_data else []
            cmd = model_data['cmd'] if 'cmd' in model_data else ''
            repo = model_data['repo'] if 'repo' in model_data else ''
            model = cls(titulo,motivation,ac,to,tags,cmd,repo)
            models.append(model)
        return models