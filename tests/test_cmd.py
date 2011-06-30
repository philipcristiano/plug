from dingus import Dingus, DingusTestCase

from plug.cmd import *
import plug.cmd as mod

#####
##
## main
##
#####

class BaseMain(DingusTestCase(main)):

    def setup(self):
        super(BaseMain, self).setup()
        self.options = Dingus('options')

    def should_parse_args(self):
        assert mod.parser.calls('parse_args')


class WhenCreating(BaseMain):

    def setup(self):
        BaseMain.setup(self)
        self.args = ['create']
        mod.parser.parse_args.return_value = (self.options, self.args)

        main()

    def should_call_create_with_options(self):
        assert mod.cmd_create.calls('()', self.options)

class WhenInstalling(BaseMain):

    def setup(self):
        BaseMain.setup(self)
        self.args = ['install']
        mod.parser.parse_args.return_value = (self.options, self.args)

        main()

    def should_call_create_with_options(self):
        assert mod.cmd_install.calls('()', self.options)

class WhenSettingUp(BaseMain):

    def setup(self):
        BaseMain.setup(self)
        self.args = ['setup']
        mod.parser.parse_args.return_value = (self.options, self.args)

        main()

    def should_call_create_with_options(self):
        assert mod.cmd_setup.calls('()', self.options)

#####
##
## cmd_create
##
#####

class BaseCmdCreate(DingusTestCase(cmd_create, ['run_commands'])):

    def setup(self):
        super(BaseCmdCreate, self).setup()
        self.options = Dingus('options')

    def assert_runs_cmd(self, cmd):
        assert mod.shlex.calls('split', cmd).once()

    def should_split_package_name(self):
        assert mod.os.path.calls('split', self.options.package)


class WhenCreatingPAckage(BaseCmdCreate):

    def setup(self):
        BaseCmdCreate.setup(self)

        cmd_create(self.options)
