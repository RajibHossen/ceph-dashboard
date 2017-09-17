"""
Ceph Wrapper class
"""
import dashboard.devopscephwrapper.docephclient as client
import dashboard.devopscephwrapper.doexceptions as exceptions


class CephWrapper(client.CephClient):
    """
    Ceph Wrapper class to communicate with client
    All the ceph API calls are defining here
    """
    def __init__(self, **params):
        super(CephWrapper, self).__init__(**params)
        self.user_agent = 'python-cephclient-wrapper'

    ###
    # root GET calls
    ###
    def df(self, detail=None, **kwargs):
        """
        get ceph cluster data usage
        :param detail:
        :param kwargs:
        :return: calls to client with appropriate urls and methods
        """
        if detail is not None:
            return self.get('df?detail={0}'
                            .format(detail), **kwargs)
        else:
            return self.get('df', **kwargs)

    def fsid(self, **kwargs):
        """
        get cluster FSID
        :param kwargs:
        :return:
        """
        return self.get('fsid', **kwargs)

    def health(self, detail=None, **kwargs):
        """
        get ceph cluster overall health with detail Parameter
        :param detail:
        :param kwargs:
        :return:
        """
        if detail is not None:
            return self.get('health?detail={0}'
                            .format(detail), **kwargs)
        else:
            return self.get('health', **kwargs)

    def quorum_status(self, **kwargs):
        """
        get Ceph cluster quorum status
        :param kwargs:
        :return:
        """
        return self.get('quorum_status', **kwargs)

    def report(self, tags=None, **kwargs):
        """
        get Ceph Cluster details report
        :param tags:
        :param kwargs:
        :return:
        """
        if tags is not None:
            return self.get('report?tags={0}'
                            .format(tags), **kwargs)
        else:
            return self.get('report', **kwargs)

    def status(self, **kwargs):
        """
        get Health status of ceph cluster
        :param kwargs:
        :return:
        """
        return self.get('status', **kwargs)

    def node_ls(self, types=None, **kwargs):
        """
        get Node listing of ceph cluster
        :param types: types of nodes such as mons/osds
        :param kwargs:
        :return:
        """
        if types is not None:
            return self.get('node/ls?type={0}'
                            .format(types), **kwargs)
        else:
            return self.get('node/ls', **kwargs)

    ###
    # root PUT calls
    ###
    def compact(self, **kwargs):
        """
        PUT compact to cluster
        :param kwargs:
        :return:
        """
        return self.put('compact', **kwargs)

    def heap(self, heapcmd, **kwargs):
        """
        Change heap size of cluster
        :param heapcmd:
        :param kwargs:
        :return:
        """
        return self.put('heap?heapcmd={0}'
                        .format(heapcmd), **kwargs)

    def injectargs(self, injected_args, **kwargs):
        """
        Inject arguments to cluster
        :param injected_args:
        :param kwargs:
        :return:
        """
        return self.put('injectargs?injected_args={0}'
                        .format(injected_args), **kwargs)

    def log(self, logtext, **kwargs):
        """
        Insert logtext to cluster
        :param logtext:
        :param kwargs:
        :return:
        """
        return self.put('log?logtext={0}'
                        .format(logtext), **kwargs)

    def quorum(self, quorumcmd, **kwargs):
        """
        Give quorum commands to cluster
        :param quorumcmd:
        :param kwargs:
        :return:
        """
        return self.put('quorum?quorumcmd={0}'
                        .format(quorumcmd), **kwargs)

    def scrub(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.put('scrub', **kwargs)

    def tell(self, target, args, **kwargs):
        """
        Give command to daemon directly
        :param target:
        :param args:
        :param kwargs:
        :return:
        """
        return self.put('tell?target={0}&args={1}'
                        .format(target, args), **kwargs)

    ###
    # auth GET calls
    ###
    def auth_export(self, entity=None, **kwargs):
        """
        Get user entity
        :param entity:
        :param kwargs:
        :return:
        """
        if entity is not None:
            return self.get('auth/export?entity={0}'
                            .format(entity), **kwargs)
        else:
            return self.get('auth/export', **kwargs)

    def auth_get(self, entity, **kwargs):
        """
        Get users info and key
        :param entity:
        :param kwargs:
        :return:
        """
        return self.get('auth/get?entity={0}'
                        .format(entity), **kwargs)

    def auth_get_key(self, entity, **kwargs):
        """
        Get only key of user
        :param entity:
        :param kwargs:
        :return:
        """
        return self.get('auth/get-key?entity={0}'
                        .format(entity), **kwargs)

    def auth_list(self, **kwargs):
        """
        Get full list of users in a cluster
        :param kwargs:
        :return:
        """
        return self.get('auth/list', **kwargs)

    def auth_print_key(self, entity, **kwargs):
        """

        :param entity:
        :param kwargs:
        :return:
        """
        return self.get('auth/print-key?entity={0}'
                        .format(entity), **kwargs)

    ###
    # auth PUT calls
    ###

    def auth_add(self, entity, caps=None, file_name=None, **kwargs):
        """
        Add a new user to cluster
        :param entity: name of user
        :param caps: {
        'mon': 'allow rwx',
        'osd': 'allow *',
        ...
        }
        :param file_name:
        :param kwargs:
        :return:
        """
        # FIXME: Implement file input
        if caps is None:
            caps = {}
        full_caps = list()
        if caps:
            for key in caps:
                permissions = caps[key].replace(' ', '+')
                full_caps.append('&caps={0}&caps={1}'
                                 .format(key, permissions))

        return self.put('auth/add?entity={0}{1}'
                        .format(entity, ''.join(full_caps)), **kwargs)

    def auth_caps(self, entity, caps=None, **kwargs):
        """
        Change user permissions/capabilities
        :param entity:
        :param caps:
        :param kwargs:
        :return:
        """
        if caps is None:
            caps = {}
        full_caps = list()
        if caps:
            for key in caps:
                permissions = caps[key].replace(' ', '+')
                full_caps.append('&caps={0}&caps={1}'
                                 .format(key, permissions))

        return self.put('auth/caps?entity={0}{1}'
                        .format(entity, ''.join(full_caps)), **kwargs)

    def auth_del(self, entity, **kwargs):
        """
        Delete user capabilities from cluster
        :param entity:
        :param kwargs:
        :return:
        """
        return self.put('auth/del?entity={0}'
                        .format(entity), **kwargs)

    def auth_get_or_create(self, entity, caps=None, file_name=None, **kwargs):
        """
        Get user if exists otherwise create user
        :param entity:
        :param caps:
        :param file_name: not implemented
        :param kwargs:
        :return:
        """
        # FIXME: Implement file input. add file_name in arguments and work with file
        if caps is None:
            caps = {}
        full_caps = list()
        if caps:
            for key in caps:
                permissions = caps[key].replace(' ', '+')
                full_caps.append('&caps={0}&caps={1}'.format(key, permissions))

        return self.put('auth/get-or-create?entity={0}{1}'
                        .format(entity, ''.join(full_caps)), **kwargs)

    def auth_get_or_create_key(self, entity, caps=None, **kwargs):
        """
        Get user key if exists otherwise create user
        :param entity:
        :param caps:
        :param kwargs:
        :return:
        """
        # FIXME: Implement file input
        if caps is None:
            caps = {}
        full_caps = list()
        if caps:
            for key in caps:
                permissions = caps[key].replace(' ', '+')
                full_caps.append('&caps={0}&caps={1}'.format(key, permissions))

        return self.put('auth/get-or-create-key?entity={0}{1}'
                        .format(entity, ''.join(full_caps)), **kwargs)

    def auth_import(self, file_name):
        """
        Import user into cluster. currently not implemented
        :param file_name:
        :return:
        self
        """
        # FIXME: Implement file input
        raise exceptions.FunctionNotImplemented()

    ###
    # config-key GET calls
    ###
    def config_key_exists(self, key, **kwargs):
        """
        Check if config key exists in cluster
        :param key:
        :param kwargs:
        :return:
        """
        return self.get('config-key/exists?key={0}'
                        .format(key), **kwargs)

    def config_key_get(self, key, **kwargs):
        """
        Get a specific config key from cluster
        :param key:
        :param kwargs:
        :return:
        """
        return self.get('config-key/get?key={0}'
                        .format(key), **kwargs)

    def config_key_list(self, **kwargs):
        """
        get list of config key
        :param kwargs:
        :return:
        """
        return self.get('config-key/list', **kwargs)

    ###
    # mds GET calls
    ###
    def mds_compat_show(self, **kwargs):
        """
        Metadata server comapat show
        :param kwargs:
        :return:
        """
        return self.get('mds/compat/show', **kwargs)

    def mds_dump(self, epoch=None, **kwargs):
        """
        get dump of metadata server with epoch specified or not
        :param epoch:
        :param kwargs:
        :return:
        """
        if epoch is not None:
            return self.get('mds/dump?epoch={0}'
                            .format(epoch), **kwargs)
        else:
            return self.get('mds/dump', **kwargs)

    def mds_getmap(self, epoch=None, **kwargs):
        """
        get metadata server map. Get all if epoch is not specified
        :param epoch:
        :param kwargs:
        :return:
        """
        kwargs['supported_body_types'] = ['binary']

        if epoch is not None:
            return self.get('mds/getmap?epoch={0}'
                            .format(epoch), **kwargs)
        else:
            return self.get('mds/getmap', **kwargs)

    def mds_stat(self, **kwargs):
        """
        MDS server stats
        :param kwargs:
        :return:
        """
        return self.get('mds/stat', **kwargs)

    ###
    # mds PUT calls
    ###
    def mds_add_data_pool(self, pool, **kwargs):
        """
        Add data pool to mds server
        :param pool:
        :param kwargs:
        :return:
        """
        return self.put('mds/add_data_pool?pool={0}'
                        .format(pool), **kwargs)

    def mds_cluster_down(self, **kwargs):
        """
        Shut down mds cluster
        :param kwargs:
        :return:
        """
        return self.put('mds/cluster_down', **kwargs)

    def mds_cluster_up(self, **kwargs):
        """
        Start mds cluster
        :param kwargs:
        :return:
        """
        return self.put('mds/cluster_up', **kwargs)

    def mds_compat_rm_compat(self, feature, **kwargs):
        """

        :param feature:
        :param kwargs:
        :return:
        """
        return self.put('mds/compat/rm_compat?feature={0}'
                        .format(feature), **kwargs)

    def mds_compat_rm_incompat(self, feature, **kwargs):
        """

        :param feature:
        :param kwargs:
        :return:
        """
        return self.put('mds/compat/rm_incompat?feature={0}'
                        .format(feature), **kwargs)

    def mds_deactivate(self, who, **kwargs):
        """
        deactivate mds cluster
        :param who:
        :param kwargs:
        :return:
        """
        return self.put('mds/deactivate?who={0}'
                        .format(who), **kwargs)

    def mds_fail(self, who, **kwargs):
        """
        Stop specific mds server from cluster
        :param who:
        :param kwargs:
        :return:
        """
        return self.put('mds/fail?who={0}'
                        .format(who), **kwargs)

    def mds_newfs(self, metadata, data, sure, **kwargs):
        """
        New filesystem for mds server
        :param metadata:
        :param data:
        :param sure:
        :param kwargs:
        :return:
        """
        return self.put('mds/newfs?metadata={0}&data={1}&sure={2}'
                        .format(metadata, data, sure), **kwargs)

    def mds_remove_data_pool(self, pool, **kwargs):
        """
        Delete data pool from mds server
        :param pool:
        :param kwargs:
        :return:
        """
        return self.put('mds/remove_data_pool?pool={0}'
                        .format(pool), **kwargs)

    def mds_rm(self, gid, who, **kwargs):
        """
        Remove mds server from cluster
        :param gid:
        :param who:
        :param kwargs:
        :return:
        """
        return self.put('mds/rm?gid={0}&who={1}'
                        .format(gid, who), **kwargs)

    def mds_rmfailed(self, who, **kwargs):
        """

        :param who:
        :param kwargs:
        :return:
        """
        return self.put('mds/rmfailed?who={0}'
                        .format(who), **kwargs)

    def mds_set_allow_new_snaps(self, sure, **kwargs):
        """
        Allow snapshot of mds
        :param sure:
        :param kwargs:
        :return:

        mds/set?key=allow_new_snaps&sure=
        """
        raise exceptions.FunctionNotImplemented()

    def mds_set_max_mds(self, maxmds, **kwargs):
        """
        Set maximum nodes for mds server
        :param maxmds:
        :param kwargs:
        :return:
        """
        return self.put('mds/set_max_mds?maxmds={0}'
                        .format(maxmds), **kwargs)

    def mds_setmap(self, epoch, **kwargs):
        """

        :param epoch:
        :param kwargs:
        :return:
        """
        return self.put('mds/setmap?epoch={0}'
                        .format(epoch), **kwargs)

    def mds_stop(self, who, **kwargs):
        """
        stop mds cluster
        :param who:
        :param kwargs:
        :return:
        """
        return self.put('mds/stop?who={0}'
                        .format(who), **kwargs)

    def mds_tell(self, who, args, **kwargs):
        """
        give commands to mds daemon
        :param who:
        :param args:
        :param kwargs:
        :return:
        """
        return self.put('mds/tell?who={0}&args={1}'
                        .format(who, args), **kwargs)

    def mds_unset_allow_new_snaps(self, sure, **kwargs):
        """
        Allow snapshot flag unset. Not implemented
        :param sure:
        :param kwargs:
        :return:

        mds/unset?key=allow_new_snaps&sure=
        """
        raise exceptions.FunctionNotImplemented()

    ###
    # mon GET calls
    ###
    def mon_dump(self, epoch=None, **kwargs):
        """
        Get monitor node dumps
        :param epoch:
        :param kwargs:
        :return:
        """
        if epoch is not None:
            return self.get('mon/dump?epoch={0}'
                            .format(epoch), **kwargs)
        else:
            return self.get('mon/dump', **kwargs)

    def mon_getmap(self, epoch=None, **kwargs):
        """
        Get monmap
        :param epoch:
        :param kwargs:
        :return:
        """
        kwargs['supported_body_types'] = ['binary']

        if epoch is not None:
            return self.get('mon/getmap?epoch={0}'
                            .format(epoch), **kwargs)
        else:
            return self.get('mon/getmap', **kwargs)

    def mon_stat(self, **kwargs):
        """
        Get monitor node stats
        :param kwargs:
        :return:
        """
        kwargs['supported_body_types'] = ['text', 'xml']

        return self.get('mon/stat', **kwargs)

    def mon_status(self, **kwargs):
        """
        Get summary status of monitor nodes
        :param kwargs:
        :return:
        """
        return self.get('mon_status', **kwargs)

    def mon_metadata(self, mon_id=None, **kwargs):
        """
        Get monitor nodes metadata
        :param mon_id:
        :param kwargs:
        :return:
        """
        if id is not None:
            return self.get('mon/metadata?id={0}'.format(mon_id), **kwargs)
        else:
            return self.get('mon/metadata', **kwargs)

    ###
    # mon PUT calls
    ###
    def mon_add(self, name, addr, **kwargs):
        """
        Add monitor nodes in cluster
        :param name:
        :param addr:
        :param kwargs:
        :return:
        """
        return self.put('mon/add?name={0}&addr={1}'
                        .format(name, addr), **kwargs)

    def mon_remove(self, name, **kwargs):
        """
        Remove monitor node from cluster
        :param name:
        :param kwargs:
        :return:
        """
        return self.put('mon/remove?name={0}'
                        .format(name), **kwargs)

    ###
    # osd GET calls
    ###
    def osd_blacklist_ls(self, **kwargs):
        """
        Get blacklisted osd nodes
        :param kwargs:
        :return:
        """
        return self.get('osd/blacklist/ls', **kwargs)

    def osd_crush_dump(self, **kwargs):
        """
        Osd nodes crush algorithm dump
        :param kwargs:
        :return:
        """
        return self.get('osd/crush/dump', **kwargs)

    def osd_crush_rule_dump(self, **kwargs):
        """
        osd nodes crush rules dump
        :param kwargs:
        :return:
        """
        return self.get('osd/crush/rule/dump', **kwargs)

    def osd_crush_rule_list(self, **kwargs):
        """
        crush rules list for osds
        :param kwargs:
        :return:
        """
        return self.get('osd/crush/rule/list', **kwargs)

    def osd_crush_rule_ls(self, **kwargs):
        """
        Listing of all osd crush rules
        :param kwargs:
        :return:
        """
        return self.get('osd/crush/rule/ls', **kwargs)

    def osd_crush_show_tunables(self, **kwargs):
        """
        osd crush show all possible tunables
        :param kwargs:
        :return:
        """
        return self.get('osd/crush/show-tunables', **kwargs)

    def osd_dump(self, epoch=None, **kwargs):
        """
        osd dump of cluster. get specified version if epoch is present
        :param epoch:
        :param kwargs:
        :return:
        """
        if epoch is not None:
            return self.get('osd/dump?epoch={0}'
                            .format(epoch), **kwargs)
        else:
            return self.get('osd/dump', **kwargs)

    def osd_find(self, osd_id, **kwargs):
        """
        Find osd node location in cluster
        :param osd_id:
        :param kwargs:
        :return:
        """
        return self.get('osd/find?id={0}'
                        .format(osd_id), **kwargs)

    def osd_getcrushmap(self, epoch=None, **kwargs):
        """
        Get osd crushdump, specified version if epoch is present
        :param epoch:
        :param kwargs:
        :return:
        """
        kwargs['supported_body_types'] = ['binary']

        if epoch is not None:
            return self.get('osd/getcrushmap?epoch={0}'
                            .format(epoch), **kwargs)
        else:
            return self.get('osd/getcrushmap', **kwargs)

    def osd_getmap(self, epoch=None, **kwargs):
        """
        Get osdmap
        :param epoch:
        :param kwargs:
        :return:
        """
        kwargs['supported_body_types'] = ['binary']

        if epoch is not None:
            return self.get('osd/getmap?epoch={0}'
                            .format(epoch), **kwargs)
        else:
            return self.get('osd/getmap', **kwargs)

    def osd_getmaxosd(self, **kwargs):
        """
        Get maximum number of osd a cluster can have
        :param kwargs:
        :return:
        """
        return self.get('osd/getmaxosd', **kwargs)

    def osd_ls(self, epoch=None, **kwargs):
        """
        list osd nodes
        :param epoch:
        :param kwargs:
        :return:
        """
        if epoch is not None:
            return self.get('osd/ls?epoch={0}'
                            .format(epoch), **kwargs)
        else:
            return self.get('osd/ls', **kwargs)

    def osd_lspools(self, auid=None, **kwargs):
        """
        osd pools list
        :param auid:
        :param kwargs:
        :return:
        """
        if auid is not None:
            return self.get('osd/lspools?auid={0}'
                            .format(auid), **kwargs)
        else:
            return self.get('osd/lspools', **kwargs)

    def osd_map(self, pool, obj, **kwargs):
        """
        get osd map with pool and object number.
        :param pool:
        :param obj:
        :param kwargs:
        :return:
        """
        return self.get('osd/map?pool={0}&object={1}'
                        .format(pool, obj), **kwargs)

    def osd_perf(self, **kwargs):
        """
        get osd performance summary
        :param kwargs:
        :return:
        """
        return self.get('osd/perf', **kwargs)

    def osd_pool_get(self, pool, var, **kwargs):
        """
        get osd with pool name and var
        :param pool:
        :param var:
        :param kwargs:
        :return:
        """
        return self.get('osd/pool/get?pool={0}&var={1}'
                        .format(pool, var), **kwargs)

    def osd_pool_stats(self, name=None, **kwargs):
        """
        get status of osd pools
        :param name:
        :param kwargs:
        :return:
        """
        if name is not None:
            return self.get('osd/pool/stats?name={0}'
                            .format(name), **kwargs)
        else:
            return self.get('osd/pool/stats', **kwargs)

    def osd_pool_ls(self, detail=None, **kwargs):
        """
        List all osd pools with details if present
        :param detail:
        :param kwargs:
        :return:
        """
        if detail is not None:
            return self.get('osd/pool/ls?detail={0}'.format(detail), **kwargs)
        else:
            return self.get('osd/pool/ls', **kwargs)

    def osd_stat(self, **kwargs):
        """
        get osd statistics
        :param kwargs:
        :return:
        """
        return self.get('osd/stat', **kwargs)

    def osd_tree(self, epoch=None, **kwargs):
        """
        get osd list in tree structure
        :param epoch:
        :param kwargs:
        :return:
        """
        if epoch is not None:
            return self.get('osd/tree?epoch={0}'
                            .format(epoch), **kwargs)
        else:
            return self.get('osd/tree', **kwargs)

    def osd_metadata(self, osd_id=None, **kwargs):
        """
        get osd metadata
        :param osd_id:
        :param kwargs:
        :return:
        """
        if id is not None:
            return self.get('osd/metadata?id={0}'.format(osd_id), **kwargs)
        else:
            return self.get('osd/metadata', **kwargs)

    def osd_df(self, output_method=None, **kwargs):
        """
        osd wise data usages
        :param output_method:
        :param kwargs:
        :return:
        """
        if output_method is not None:
            return self.get('osd/df?output_method={0}'.format(output_method), **kwargs)
        else:
            return self.get('osd/df', **kwargs)

    def osd_utilization(self, **kwargs):
        """
        get utilization of all osds
        :param kwargs:
        :return:
        """
        return self.get('osd/utilization', **kwargs)


    ###
    # osd PUT calls
    ###
    def osd_blacklist(self, blacklistop, addr, expire, **kwargs):
        """
        put an osd into blacklist
        :param blacklistop:
        :param addr:
        :param expire:
        :param kwargs:
        :return:
        """
        return self.put('osd/blacklist?blacklistop={0}&addr={1}&expire={2}'
                        .format(blacklistop, addr, expire), **kwargs)

    def osd_create(self, uuid, **kwargs):
        """
        Create osd
        :param uuid: unique id for osd
        :param kwargs:
        :return:
        """
        return self.put('osd/create?uuid={0}'
                        .format(uuid), **kwargs)

    def osd_crush_add(self, osd_id, weight, args, **kwargs):
        """
        Add new osd crush rule
        :param osd_id:
        :param weight:
        :param args:
        :param kwargs:
        :return:
        """
        return self.put('osd/crush/add?id={0}&weight={1}&args={2}'
                        .format(osd_id, weight, args), **kwargs)

    def osd_crush_add_bucket(self, name, osd_type, **kwargs):
        """
        Add bucket in crush rules
        :param name:
        :param osd_type:
        :param kwargs:
        :return:
        """
        return self.put('osd/crush/add-bucket?name={0}&type={1}'
                        .format(name, osd_type), **kwargs)

    def osd_crush_create_or_move(self, osd_id, weight, args, **kwargs):
        """
        create if not exist otherwise move to different position.
        :param osd_id:
        :param weight:
        :param args:
        :param kwargs:
        :return:
        """
        return self.put('osd/crush/create-or-move?id={0}&weight={1}&args={2}'
                        .format(osd_id, weight, args), **kwargs)

    def osd_crush_link(self, name, args, **kwargs):
        """
        List one crush rule to others
        :param name:
        :param args:
        :param kwargs:
        :return:
        """
        return self.put('osd/crush/link?name={0}&args={2}'
                        .format(name, args), **kwargs)

    def osd_crush_move(self, name, args, **kwargs):
        """

        :param name:
        :param args:
        :param kwargs:
        :return:
        """
        return self.put('osd/crush/move?name={0}&args={1}'
                        .format(name, args), **kwargs)

    def osd_crush_remove(self, name, ancestor, **kwargs):
        """
        Remove crush rule from cluster
        :param name:
        :param ancestor:
        :param kwargs:
        :return:
        """
        return self.put('osd/crush/remove?name={0}&ancestor={1}'
                        .format(name, ancestor), **kwargs)

    def osd_crush_reweight(self, name, weight, **kwargs):
        """
        change the weight calculation of cluster. new calculation will start.
        :param name:
        :param weight:
        :param kwargs:
        :return:
        """
        return self.put('osd/crush/reweight?name={0}&weight={1}'
                        .format(name, weight), **kwargs)

    def osd_crush_rm(self, name, ancestor, **kwargs):
        """
        Delete crush rules
        :param name:
        :param ancestor:
        :param kwargs:
        :return:
        """
        return self.put('osd/crush/rm?name={0}&ancestor={1}'
                        .format(name, ancestor), **kwargs)

    def osd_crush_rule_create_simple(self, name, root, osd_type, **kwargs):
        """

        :param name:
        :param root:
        :param osd_type:
        :param kwargs:
        :return:
        """
        return self.put(
            'osd/crush/rule/create-simple?name={0}&root={1}&type={2}'
            .format(name, root, osd_type), **kwargs)

    def osd_crush_rule_rm(self, name, **kwargs):
        """
        Remove crush rule from crush algorithms
        :param name:
        :param kwargs:
        :return:
        """
        return self.put('osd/crush/rule/rm?name={0}'
                        .format(name), **kwargs)

    def osd_crush_set(self, osd_id, name, weight, args, **kwargs):
        """
        Set crush rule
        :param osd_id:
        :param name:
        :param weight:
        :param args:
        :param kwargs:
        :return:
        """
        return self.put('osd/crush/set?id={0}&weight={1}&args={2}'
                        .format(osd_id, name, weight, args), **kwargs)

    def osd_crush_tunables(self, profile, **kwargs):
        """
        change tunable profile of osd crush
        :param profile:
        :param kwargs:
        :return:
        """
        return self.put('osd/crush/tunables?profile={0}'
                        .format(profile), **kwargs)

    def osd_crush_unlink(self, name, ancestor, **kwargs):
        """

        :param name:
        :param ancestor:
        :param kwargs:
        :return:
        """
        return self.put('osd/crush/unlink?name={0}&ancestor={1}'
                        .format(name, ancestor), **kwargs)

    def osd_deep_scrub(self, who, **kwargs):
        """
        start deep scrubing in osd
        :param who:
        :param kwargs:
        :return:
        """
        return self.put('osd/deep-scrub?who={0}'
                        .format(who), **kwargs)

    def osd_down(self, ids, **kwargs):
        """
        Stop osd in cluster
        :param ids:
        :param kwargs:
        :return:
        """
        return self.put('osd/down?ids={0}'
                        .format(ids), **kwargs)

    def osd_in(self, ids, **kwargs):
        """
        Enter an osd into cluster
        :param ids:
        :param kwargs:
        :return:
        """
        return self.put('osd/in?ids={0}'
                        .format(ids), **kwargs)

    def osd_lost(self, osd_id, sure, **kwargs):
        """

        :param osd_id:
        :param sure:
        :param kwargs:
        :return:
        """
        return self.put('osd/lost?id={0}&sure={1}'
                        .format(osd_id, sure), **kwargs)

    def osd_out(self, ids, **kwargs):
        """
        remove osd out of cluster
        :param ids:
        :param kwargs:
        :return:
        """
        return self.put('osd/out?ids={0}'
                        .format(ids), **kwargs)

    def osd_pool_create(self, pool, pg_num, pgp_num, **kwargs):
        """
        Create osd pool
        :param pool: name of pool
        :param pg_num: placement_group number
        :param pgp_num:
        :param kwargs:
        :return:
        """
        return self.put(
            'osd/pool/create?pool={0}&pg_num={1}&pgp_num={2}'
            .format(pool, pg_num, pgp_num), **kwargs)

    def osd_pool_delete(self, pool, sure, **kwargs):
        """
        Delete osd pool
        :param pool: name
        :param sure: --yes-i-really-mean-it
        :param kwargs:
        :return:
        """
        return self.put('osd/pool/delete?pool={0}&sure={1}'
                        .format(pool, sure), **kwargs)

    def osd_pool_param(self, pool, var, **kwargs):
        """
        get osd pool parameters
        :param pool:
        :param var:
        :param kwargs:
        :return:
        """
        return self.put('osd/pool/get?pool={0}&var={1}'
                        .format(pool, var), **kwargs)

    def osd_pool_mksnap(self, pool, snap, **kwargs):
        """
        Take snapshot of osd pool
        :param pool:
        :param snap:
        :param kwargs:
        :return:
        """
        return self.put('osd/pool/mksnap?pool={0}&snap={1}'
                        .format(pool, snap), **kwargs)

    def osd_pool_rename(self, srcpool, destpool, **kwargs):
        """
        Rename pool name
        :param srcpool:
        :param destpool:
        :param kwargs:
        :return:
        """
        return self.put('osd/pool/rename?srcpool={0}&destpool={1}'
                        .format(srcpool, destpool), **kwargs)

    def osd_pool_rmsnap(self, pool, snap, **kwargs):
        """
        delete snapshot of osd pool
        :param pool:
        :param snap:
        :param kwargs:
        :return:
        """
        return self.put('osd/pool/rmsnap?pool={0}&snap={1}'
                        .format(pool, snap), **kwargs)

    def osd_set_pool_param(self, pool, var, **kwargs):
        """
        set osd pool parameters
        :param pool: pool name
        :param var: parameter name
        :param kwargs:
        :return:
        """
        return self.put('osd/pool/set?pool={0}&var={1}'
                        .format(pool, var), **kwargs)

    def osd_set_pool_quota(self, pool, field, **kwargs):
        """
        set quota of osd in a pool
        :param pool:
        :param field:
        :param kwargs:
        :return:
        """
        return self.put('osd/pool/set-quota?pool={0}&field={1}'
                        .format(pool, field), **kwargs)

    def osd_repair(self, pool, who, **kwargs):
        """
        start repairing osd
        :param pool:
        :param who:
        :param kwargs:
        :return:
        """
        return self.put('osd/repair?who={0}'
                        .format(pool, who), **kwargs)

    def osd_reweight(self, id, weight, **kwargs):
        """
        change weight of single osd node
        :param id: id of osd
        :param weight:
        :param kwargs:
        :return:
        """
        return self.put('osd/reweight?id={0}&weight={1}'
                        .format(id, weight), **kwargs)

    def osd_reweight_by_utilization(self, oload, **kwargs):
        """
        start reweight entire cluster osd using utilization
        :param oload:
        :param kwargs:
        :return:
        """
        return self.put('osd/reweight-by-utilization?oload={0}'
                        .format(oload), **kwargs)

    def osd_remove(self, ids, **kwargs):
        """
        delete osd node
        :param ids:
        :param kwargs:
        :return:
        """
        return self.put('osd/rm?ids={0}'
                        .format(ids), **kwargs)

    def osd_scrub(self, who, **kwargs):
        """
        start scrubing in osd
        :param who:
        :param kwargs:
        :return:
        """
        return self.put('osd/scrub?who={0}'
                        .format(who), **kwargs)

    def osd_set_key(self, key, **kwargs):
        """

        :param key:
        :param kwargs:
        :return:
        """
        return self.put('osd/set?key={0}'
                        .format(key), **kwargs)

    def osd_setmaxosd(self, newmax, **kwargs):
        """

        :param newmax:
        :param kwargs:
        :return:
        """
        return self.put('osd/setmaxosd?newmax={0}'
                        .format(newmax), **kwargs)

    def osd_thrash(self, num_epochs, **kwargs):
        """

        :param num_epochs:
        :param kwargs:
        :return:
        """
        return self.put('osd/thrash?num_epochs={0}'
                        .format(num_epochs), **kwargs)

    def osd_tier_add(self, pool, tierpool, **kwargs):
        """

        :param pool:
        :param tierpool:
        :param kwargs:
        :return:
        """
        return self.put('osd/tier/add?pool={0}&tierpool={1}'
                        .format(pool, tierpool), **kwargs)

    def osd_tier_cachemode(self, pool, mode, **kwargs):
        """

        :param pool:
        :param mode:
        :param kwargs:
        :return:
        """
        return self.put('osd/tier/cache-mode?pool={0}&mode={1}'
                        .format(pool, mode), **kwargs)

    def osd_tier_remove(self, pool, tierpool, **kwargs):
        """

        :param pool:
        :param tierpool:
        :param kwargs:
        :return:
        """
        return self.put('osd/tier/remove?pool={0}&tierpool={1}'
                        .format(pool, tierpool), **kwargs)

    def osd_tier_remove_overlay(self, pool, **kwargs):
        """

        :param pool:
        :param kwargs:
        :return:
        """
        return self.put('osd/tier/remove-overlay?pool={0}'
                        .format(pool), **kwargs)

    def osd_tier_set_overlay(self, pool, overlaypool, **kwargs):
        """

        :param pool:
        :param overlaypool:
        :param kwargs:
        :return:
        """
        return self.put('osd/tier/set-overlay?pool={0}&overlaypool={1}'
                        .format(pool, overlaypool), **kwargs)

    def osd_unset(self, key, **kwargs):
        """

        :param key:
        :param kwargs:
        :return:
        """
        return self.put('osd/unset?key={0}'
                        .format(key), **kwargs)

    ###
    # pg GET calls
    ###
    def pg_debug(self, debugop, **kwargs):
        """
        Get debug op of placement groups
        :param debugop:
        :param kwargs:
        :return:
        """
        kwargs['supported_body_types'] = ['text', 'xml']

        return self.get('pg/debug?debugop={0}'
                        .format(debugop), **kwargs)

    def pg_dump(self, dumpcontents=None, **kwargs):
        """
        Get pg dumps with dumpcontents if present
        :param dumpcontents:
        :param kwargs:
        :return:
        """
        if dumpcontents is not None:
            return self.get('pg/dump?dumpcontents={0}'
                            .format(dumpcontents), **kwargs)
        else:
            return self.get('pg/dump', **kwargs)

    def pg_dump_json(self, dumpcontents=None, **kwargs):
        """
        Get pg dump in json format
        :param dumpcontents:
        :param kwargs:
        :return:
        """
        if dumpcontents is not None:
            return self.get('pg/dump_json?dumpcontents={0}'
                            .format(dumpcontents), **kwargs)
        else:
            return self.get('pg/dump_json', **kwargs)

    def pg_dump_pools_json(self, **kwargs):
        """
        placement group dump of pools in json format

        :param kwargs:
        :return:
        """
        return self.get('pg/dump_pools_json', **kwargs)

    def pg_dump_stuck(self, stuckops=None, **kwargs):
        """
        Stucked placement group dump
        :param stuckops:
        :param kwargs:
        :return:
        """
        if stuckops is not None:
            return self.get('pg/dump_stuck?stuckops={0}'
                            .format(stuckops), **kwargs)
        else:
            return self.get('pg/dump_stuck', **kwargs)

    def pg_getmap(self, **kwargs):
        """
        placement group maps
        :param kwargs:
        :return:
        """
        kwargs['supported_body_types'] = ['binary']

        return self.get('pg/getmap', **kwargs)

    def pg_map(self, pgid, **kwargs):
        """

        :param pgid:
        :param kwargs:
        :return:
        """
        return self.get('pg/map?pgid={0}'
                        .format(pgid), **kwargs)

    def pg_stat(self, **kwargs):
        """
        get placement group stats
        :param kwargs:
        :return:
        """
        return self.get('pg/stat', **kwargs)

    def pg_ls_by_pool(self, pool_id, states, **kwargs):
        """
        Get placement groups list by pool
        :param pool_id:
        :param states:
        :param kwargs:
        :return:
        """

        if pool_id and states:
            return self.get('pg/ls?pool={0}&states={1}'.format(pool_id, states), **kwargs)
        elif pool_id and not states:
            return self.get('pg/ls?pool={0}'.format(pool_id), **kwargs)
        elif not pool_id and states:
            return self.get('pg/ls?states={0}'.format(states), **kwargs)
        else:
            return self.get('pg/ls', **kwargs)

    def pg_ls_by_osd(self, osd_id, pool_id, states, **kwargs):
        """
        Get placement group list by osd
        :param osd_id:
        :param pool_id:
        :param states:
        :param kwargs:
        :return:
        """

        if pool_id and states:
            return self.get('pg/ls-by-osd?osd={0}&pool={1}&states={2}'
                            .format(osd_id, pool_id, states), **kwargs)
        elif pool_id and not states:
            return self.get('pg/ls-by-osd?osd={0}&pool={1}'.format(osd_id, pool_id), **kwargs)
        elif not pool_id and states:
            return self.get('pg/ls-by-osd?osd={0}&states={1}'.format(osd_id, states), **kwargs)
        else:
            return self.get('pg/ls-by-osd?osd={0}'.format(osd_id), **kwargs)

    def pg_ls_by_primary(self, osd_id, pool_id, states, **kwargs):
        """
        Get placement group list by primary osd
        :param osd_id:
        :param pool_id:
        :param states:
        :param kwargs:
        :return:
        """
        if pool_id and states:
            return self.get('pg/ls-by-primary?osd={0}&pool={1}&states={2}'
                            .format(osd_id, pool_id, states), **kwargs)
        elif pool_id and not states:
            return self.get('pg/ls-by-primary?osd={0}&pool={1}'.format(osd_id, pool_id), **kwargs)
        elif not pool_id and states:
            return self.get('pg/ls-by-primary?osd={0}&states={1}'.format(osd_id, states), **kwargs)
        else:
            return self.get('pg/ls-by-primary?osd={0}'.format(osd_id), **kwargs)

    ###
    # tell GET calls
    ###
    def tell_debug_dump_missing(self, pg_id, filename, **kwargs):
        """
        Give commands to pg daemon
        :param pg_id:
        :param filename:
        :param kwargs:
        :return:
        """
        return self.get('tell/{0}/debug_dump_missing?filename={1}'
                        .format(pg_id, filename), **kwargs)

    def tell_dump_pg_recovery_stats(self, pg_id, **kwargs):
        """
        Give commands for pg recovery
        :param pg_id:
        :param kwargs:
        :return:
        """
        return self.get('tell/{0}/dump_pg_recovery_stats'
                        .format(pg_id), **kwargs)

    def tell_list_missing(self, pg_id, offset, **kwargs):
        """
        get missing pg
        :param pg_id:
        :param offset:
        :param kwargs:
        :return:
        """
        return self.get('tell/{0}/list_missing?offset={1}'
                        .format(pg_id, offset), **kwargs)

    def tell_query(self, pg_id, **kwargs):
        """
        give query to daemon
        :param pg_id:
        :param kwargs:
        :return:
        """
        return self.get('tell/{0}/query'
                        .format(pg_id), **kwargs)

    def tell_version(self, pg_id, **kwargs):
        """
        Get version of cluster
        :param pg_id:
        :param kwargs:
        :return:
        """
        return self.get('tell/{0}/version'
                        .format(pg_id), **kwargs)
