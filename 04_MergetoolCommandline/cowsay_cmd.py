import cmd
import cowsay
import shlex

class Arguments:
    def __init__(self, args, defaults):
        self.args = args
        self.defaults = defaults
        
DICT = {
    "cow": cowsay.list_cows(),
    "wrap_text": ["True", "False"],
    "eyes": ["BB", "Oo", "oO", "QQ", "II"],
    "tongue": ["O", "W", "S", "$", "U"],
    
}
        
        
cowsay_args = Arguments(['message', 'cow', 'eyes', 'tongue'], [None, 'default', 'oo', '  '])
cowlist_args = Arguments(['cow_path'], [cowsay.COW_PEN])
cowthink_args = Arguments(['message', 'cow', 'eyes', 'tongue'], [None, 'default', 'oo', '  '])
makebubble_args = Arguments(['text', 'wrap_text', 'width'], [None, "True", 40])

class CowsayShell(cmd.Cmd):
    intro = 'Welcome to the Cowsay Shell.   Type help or ? to list commands.\n'
    prompt = '(cowsay) '
    file = None
    
    @staticmethod
    def parse(command_info, provided_args):
        args = shlex.split(provided_args)
        args_cnt = len(args)
        cmd_args_cnt = len(command_info.args)
        cnt_iter = min(args_cnt, cmd_args_cnt)
        
        args_dict = {}
        for i in range(cnt_iter):
            args_dict[command_info.args[i]] = args[i]
        for i in range(cnt_iter, cmd_args_cnt):
            args_dict[command_info.args[i]] = command_info.defaults[i]
        
        return args_dict
    
    def get_auto_compl(self, argname, start = None):
        if start:
            return [i for i in DICT[argname] if i.startswith(start)]
        else:
            return DICT[argname]
        
        

    def do_cowsay(self, arg):
        """
        cowsay message [cow] [eyes] [tongue]
        
        Similar to the cowsay command. Parameters are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string
        

        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        """
        print(cowsay.cowsay(**self.parse(cowsay_args, arg)))
        
    def complete_cowsay(self, text, line, begidx, endidx):
        args = shlex.split(line)

        if line[-1] == " ":
            start = None
            last_arg = len(args) - 1
        else:
            start = args[-1]
            last_arg = len(args) - 2
            
        argname = cowsay_args.args[last_arg]
        return self.get_auto_compl(argname, start)
        
    def do_exit(self, arg):
        """Quit Cowsay"""
        return True
    
    def do_list_cows(self, arg):
        """Lists all cow file names in the given directory or in COW_PEN"""
        print(*cowsay.list_cows(**self.parse(cowlist_args, arg)))
    
    def complete_list_cows(self, text, line, begidx, endidx):
        args = shlex.split(line)

        if line[-1] == " ":
            start = None
            last_arg = len(args) - 1
        else:
            start = args[-1]
            last_arg = len(args) - 2
            
        argname = cowlist_args.args[last_arg]
        return self.get_auto_compl(argname, start)
        
        
    def do_cowthink(self, arg):
        """
        cowthink message [cow] [eyes] [tongue]
        
        Similar to the cowthink command. Parameters are listed with their
        corresponding options in the cowthink command. Returns the resulting
        cowthink string
        

        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        """
        print(cowsay.cowthink(**self.parse(cowthink_args, arg)))
        
    def complete_cowthink(self, text, line, begidx, endidx):
        args = shlex.split(line)

        if line[-1] == " ":
            start = None
            last_arg = len(args) - 1
        else:
            start = args[-1]
            last_arg = len(args) - 2
            
        argname = cowthink_args.args[last_arg]
        return self.get_auto_compl(argname, start)
        
    def do_make_bubble(self, arg):
        '''
        make_bubble text [wrap_text]
        make_bubble text [wrap_text] [width]

        Wraps text if wrap_text is true, then pads text and sets inside a bubble. This is the text that appears above the cows
        '''
        args_dict = self.parse(makebubble_args, arg)
        args_dict["width"] = int(args_dict["width"])
        args_dict["wrap_text"] = args_dict["wrap_text"] == "True"
        print(cowsay.make_bubble(**args_dict))
        
    def complete_make_bubble(self, text, line, begidx, endidx):
        args = shlex.split(line)

        if line[-1] == " ":
            start = None
            last_arg = len(args) - 1
        else:
            start = args[-1]
            last_arg = len(args) - 2
            
        argname = makebubble_args.args[last_arg]
        return self.get_auto_compl(argname, start)
        
        
        

        
        
        


if __name__ == '__main__':
    CowsayShell().cmdloop()