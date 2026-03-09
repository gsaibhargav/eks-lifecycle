#!/usr/bin/env python3

class EKSUtility(object):
    def __init__(self,client):
        self.client = client

    def get_cluster_inventory(self, version_status=None) -> list:
        """Return a list of EKS cluster and their versions"""
        cluster_versions=[]
        paginator = self.client.get_paginator('list_clusters')
        for page in paginator.paginate():
            for cluster in page['clusters']:
                # describe cluster to fetch all the details
                desc_response = self.client.describe_cluster(name=cluster)['cluster']
                version = desc_response['version']
                cluster_versions.append({
                    'name': cluster,
                    'version': version
                })
        return(cluster_versions)

    def get_eks_version_status(self) -> dict:
        """Return a map of all EKS versions and their support status"""
        version_status={}
        paginator = self.client.get_paginator('describe_cluster_versions')
        for page in paginator.paginate():
            for ver in page['clusterVersions']:
                version_status[ver['clusterVersion']]={
                    'status': ver['versionStatus'],
                    'end_standard_date': ver['endOfStandardSupportDate'],
                    'end_extend_date': ver['endOfExtendedSupportDate']
                }
        return(version_status)
    
    def get_cluster_addon_status(self, cluster_name, cluster_version) -> list:
        """Return updates for addons of a provided cluster"""
        addon_updates=[]
        addons=[]
        # list all addons
        paginator = self.client.get_paginator('list_addons')
        for page in paginator.paginate(clusterName=cluster_name):
            addons.extend(page['addons'])

        # latest addon versions
        ver_paginator = self.client.get_paginator('describe_addon_versions')
        for addon in addons:
            latest_ver=None
            current=self.client.describe_addon(clusterName=cluster_name,addonName=addon)['addon']
            current_ver=current['addonVersion']

            for page in ver_paginator.paginate(addonName=addon,kubernetesVersion=cluster_version):
                # most recent version is listed first
                if page['addons'] and page['addons'][0]['addonVersions']:
                    latest_ver=page['addons'][0]['addonVersions'][0]['addonVersion']
                    break
            
            if(latest_ver is not None and latest_ver != current_ver):
                addon_updates.append({
                    'addon': addon,
                    'current_version': current_ver,
                    'latest_version': latest_ver
                })
        return(addon_updates)


