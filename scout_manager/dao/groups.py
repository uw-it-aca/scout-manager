from restclients.gws import GWS

def get_members(group):
    gws = GWS()
    members = gws.get_effective_members(group)
    return members