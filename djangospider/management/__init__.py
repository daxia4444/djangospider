
import os
import sys
from djangospider.utils.termcolor import colored
import pkgutil
from argparse import ArgumentParser
from collections import  defaultdict
from importlib import import_module




def load_command_class(app_name, name):
    """
    Given a command name and an application name, returns the Command
    class instance. All errors raised by the import process
    (ImportError, AttributeError) are allowed to propagate.
    """

    module = import_module('%s.commands.%s' % (app_name, name))
    return module.Command()



def get_commands():

    commands = {name: 'djangospider.management' for name in find_commands()}
    return commands




def find_commands():
    """
    Given a path to a management directory, returns a list of all the command
    names that are available.

    Returns an empty list if no commands are defined.
    """

    path=os.path.split(os.path.realpath(__file__))[0]
    command_dir = os.path.join(path, 'commands')
    import pdb
    #pdb.set_trace()
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]



class CommandParser(ArgumentParser):
    """
    Customized ArgumentParser class to improve some error messages and prevent
    SystemExit in several occasions, as SystemExit is unacceptable when a
    command is called programmatically.
    """
    def __init__(self, cmd, **kwargs):
        self.cmd = cmd
        super(CommandParser, self).__init__(**kwargs)

    def parse_args(self, args=None, namespace=None):
        # Catch missing argument for a better error message
        if (hasattr(self.cmd, 'missing_args_message') and
                not (args or any(not arg.startswith('-') for arg in args))):
            self.error(self.cmd.missing_args_message)
        return super(CommandParser, self).parse_args(args, namespace)

    def error(self, message):
        if self.cmd._called_from_command_line:
            super(CommandParser, self).error(message)
        else:
            raise CommandError("Error: %s" % message)






class ManagementUtility(object):
    """

    A ManagementUtility has a number of commands, which can be manipulated
    by editing the self.commands dictionary.
    """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.settings_exception = None

    def main_help_text(self, commands_only=False):
        """
        Returns the script's main help text, as a string.
        """

        usage = [
            "",
            "Type '%s help <subcommand>' for help on a specific subcommand." % self.prog_name,
            "",
            "Available subcommands:",
        ]
        
        #commands_dict=find_commands()
        commands_dict = defaultdict(lambda: [])
        app='djangospider'

        import pdb
        #pdb.set_trace()
        text=colored('[djangospider]','red')
        usage.append(text)

        '''
        for name in find_commands():            
            commands_dict[app].append(name)
        '''
        for name in sorted(find_commands()):
            usage.append("    %s" % name)

        # Output an extra note if settings are not properly configured
        return '\n'.join(usage)

    def fetch_command(self, subcommand):
        """
        Tries to fetch the given subcommand, printing a message with the
        appropriate command called from the command line (usually
        "django-admin" or "manage.py") if it can't be found.
        """
        # Get commands outside of try block to prevent swallowing exceptions

        commands = get_commands()
        try:
            app_name = commands[subcommand]
        except KeyError:
            sys.stderr.write("Unknown command: %r\nType '%s help' for usage.\n" %
                (subcommand, self.prog_name))
            sys.exit(1)
        import pdb
        #pdb.set_trace()
        klass = load_command_class(app_name, subcommand)

        #pdb.set_trace()
        return klass


    def execute(self):
        """
        Given the command-line arguments, this figures out which subcommand is
        being run, creates a parser appropriate to that command, and runs it.
        """

        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'  # Display help if no arguments were given.

        # Preprocess options to extract --settings and --pythonpath.
        # These options could affect the commands that are available, so they
        # must be processed early.
        parser = CommandParser(None, usage="%(prog)s subcommand [options] [args]", add_help=False)
        parser.add_argument('--settings')
        parser.add_argument('--pythonpath')
        parser.add_argument('args', nargs='*')  # catch-all
        try:
            options, args = parser.parse_known_args(self.argv[2:])

        except Exception as e:
            pass  # Ignore any option errors at this point.


        import pdb
        #pdb.set_trace()
        if subcommand == 'help':
            if len(options.args) < 1:
                sys.stdout.write(self.main_help_text() + '\n')
            else:
                self.fetch_command(options.args[0]).print_help(self.prog_name, options.args[0])
        # Special-cases: We want 'django-admin --version' and
        # 'django-admin --help' to work, for backwards compatibility.
        elif subcommand == 'version' or self.argv[1:] == ['--version']:
            sys.stdout.write("djangospider 0.1")
        elif self.argv[1:] in (['--help'], ['-h']):
            sys.stdout.write(self.main_help_text() + '\n')
        else:
            self.fetch_command(subcommand).run_from_argv(self.argv)



def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    argv=sys.argv
    utility = ManagementUtility(argv)
    utility.execute()




if __name__ == "__main__":
    argv=sys.argv
    utility = ManagementUtility(argv)
    utility.execute()