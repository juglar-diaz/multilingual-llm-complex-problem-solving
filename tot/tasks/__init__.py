def get_task(name, file=None, lang='en'):
    if name == 'game24':
        from .game24 import Game24Task
        return Game24Task(file, lang)
    elif name == 'text':
        from .text import TextTask
        return TextTask(file, lang)
    elif name == 'crosswords':
        from .crosswords import MiniCrosswordsTask
        return MiniCrosswordsTask(file)
    else:
        raise NotImplementedError