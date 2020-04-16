import ibeis
import utool as ut

'''
databases
  - sea turtles
  - sea dragons
  - mantas
  - hammerheads
  - right whale heads
  - [SKIPPED] spotted dolphin dorsal fins
'''

################################################################################

# Sea Turtles
ibs = ibeis.opendb(dbdir='/data/ibeis/ST_Master')

all_aid_list = ibs.get_valid_aids()
all_species_list = ibs.get_annot_species(all_aid_list)
all_flag_list = [
    all_species in set(['turtle_green+head', 'turtle_hawksbill+head', 'turtle_oliveridley+head'])
    for all_species in all_species_list
]
delete_aid_list = ut.compress(all_aid_list, all_flag_list)
ibs.delete_annots(delete_aid_list)

species_list = [
    'turtle_green',
    'turtle_green+head',
    'turtle_hawksbill',
    'turtle_hawksbill+head',
    'turtle_oliveridley',
    'turtle_oliveridley+head',
]

species_mapping = {}

viewpoint_mapping = {
    species: {
        'left'       : 'left',
        'frontleft'  : 'front',
        'front'      : 'front',
        'frontright' : 'front',
        'right'      : 'right',
        'backright'  : 'back',
        'back'       : 'back',
        'backleft'   : 'back',
        'up'         : 'up',
        'upleft'     : 'left',
        'upfront'    : 'front',
        'upright'    : 'right',
        'upback'     : 'back',
        'down'       : 'down',
        'downleft'   : 'left',
        'downfront'  : 'front',
        'downright'  : 'right',
        'downback'   : 'back',
        None         : None,
    }
    for species in species_list
}

src_path = ibs.export_to_coco(species_list, species_mapping=species_mapping, viewpoint_mapping=viewpoint_mapping, include_parts=True, require_image_reviewed=True)
dst_path = '/data/public/datasets/orientation.seaturtle.coco'
ut.move(src_path, dst_path)

################################################################################

# Sea Drgons
ibs = ibeis.opendb(dbdir='/data/ibeis/SD_Master')

all_aid_list = ibs.get_valid_aids()
all_species_list = ibs.get_annot_species(all_aid_list)
all_flag_list = [
    all_species in set(['seadragon_leafy+head', 'seadragon_weedy+head'])
    for all_species in all_species_list
]
delete_aid_list = ut.compress(all_aid_list, all_flag_list)
ibs.delete_annots(delete_aid_list)

species_list = [
    'seadragon_leafy',
    'seadragon_weedy',
    'seadragon_leafy+head',
    'seadragon_weedy+head',
]

species_mapping = {}

viewpoint_mapping = {
    'seadragon_leafy': {
        'left'       : 'left',
        'frontleft'  : 'front',
        'front'      : 'front',
        'frontright' : 'front',
        'right'      : 'right',
        'backright'  : 'back',
        'backleft'   : 'back',
        'back'       : 'back',
        'upleft'     : 'left',
        'downleft'   : 'left',
        'upfront'    : 'front',
        'upright'    : 'right',
        'downright'  : 'right',
        'downback'   : 'back',
        'up'         : 'up',
        'down'       : 'down',
        None         : None,
    },
    'seadragon_weedy': {
        'left'       : 'left',
        'frontleft'  : 'frontleft',
        'front'      : 'front',
        'frontright' : 'frontright',
        'right'      : 'right',
        'backright'  : 'backright',
        'back'       : 'back',
        'backleft'   : 'backleft',
        'upleft'     : 'left',
        'upright'    : 'right',
        'downleft'   : 'left',
        'downright'  : 'right',
        'up'         : 'up',
        'downfront'  : 'front',
        'upfront'    : 'front',
        'upback'     : 'bacl',
        None         : None,
    },
    'seadragon_leafy+head': {
        'left'       : 'left',
        'frontleft'  : 'front',
        'front'      : 'front',
        'frontright' : 'front',
        'right'      : 'right',
        'backleft'   : 'back',
        'backright'  : 'back',
        'back'       : 'back',
        'upleft'     : 'left',
        'downleft'   : 'left',
        'upfront'    : 'front',
        'upright'    : 'right',
        'downright'  : 'right',
        'downback'   : 'back',
        'up'         : 'up',
        'down'       : 'down',
        None         : None,
    },
    'seadragon_weedy+head': {
        'left'       : 'left',
        'frontleft'  : 'frontleft',
        'front'      : 'front',
        'frontright' : 'frontright',
        'right'      : 'right',
        'backright'  : 'backright',
        'back'       : 'back',
        'backleft'   : 'backleft',
        'upleft'     : 'left',
        'upright'    : 'right',
        'downleft'   : 'left',
        'downright'  : 'right',
        'up'         : 'up',
        'downfront'  : 'front',
        'upfront'    : 'front',
        'upback'     : 'back',
        None         : None,
    },
}

src_path = ibs.export_to_coco(species_list, species_mapping=species_mapping, viewpoint_mapping=viewpoint_mapping, include_parts=True, require_image_reviewed=True)
dst_path = '/data/public/datasets/orientation.seadragon.coco'
ut.move(src_path, dst_path)

################################################################################

# Manta Rays
ibs = ibeis.opendb(dbdir='/data/ibeis/MM_Master')

# all_gid_list = ibs.get_valid_gids()
# all_review_list = ibs.get_image_reviewed(all_gid_list)
# reviewed_gid_list = ut.compress(all_gid_list, all_review_list)
# reviewed_aid_list = ut.flatten(ibs.get_image_aids(reviewed_gid_list))
# reviewed_species_list = ibs.get_annot_species(reviewed_aid_list)

species_list = [
    'manta_ray_giant',
]

viewpoint_mapping = {
    'manta_ray_giant': {
        'back'       : 'back',
        'backleft'   : 'back',
        'backright'  : 'back',
        'down'       : 'down',
        'downback'   : 'downback',
        'downfront'  : 'downfront',
        'downleft'   : 'downleft',
        'downright'  : 'downright',
        'front'      : 'front',
        'frontleft'  : 'front',
        'frontright' : 'front',
        'ignore'     : None,
        'left'       : 'left',
        'right'      : 'right',
        'up'         : 'up',
        'upback'     : 'up',
        'upfront'    : 'up',
        'upleft'     : 'up',
        'upright'    : 'up',
    }
}

src_path = ibs.export_to_coco(species_list, species_mapping=species_mapping, viewpoint_mapping=viewpoint_mapping, include_parts=False, require_image_reviewed=True)
dst_path = '/data/public/datasets/orientation.mantaray.coco'
ut.move(src_path, dst_path)

################################################################################

# Hammerhead
ibs = ibeis.opendb(dbdir='/data/ibeis/HH_Master')

# all_gid_list = ibs.get_valid_gids()
# all_review_list = ibs.get_image_reviewed(all_gid_list)
# reviewed_gid_list = ut.compress(all_gid_list, all_review_list)
# reviewed_aid_list = ut.flatten(ibs.get_image_aids(reviewed_gid_list))
# reviewed_species_list = ibs.get_annot_species(reviewed_aid_list)

species_list = [
    'shark_hammerhead',
]

viewpoint_mapping = {}

src_path = ibs.export_to_coco(species_list, species_mapping=species_mapping, viewpoint_mapping=viewpoint_mapping, include_parts=False, require_image_reviewed=True)
dst_path = '/data/public/datasets/orientation.hammerhead.coco'
ut.move(src_path, dst_path)

################################################################################

# Right Whale Heads
ibs = ibeis.opendb(dbdir='/data/ibeis/RW_Master')

all_gid_list = ibs.get_valid_gids()
all_review_list = ibs.get_image_reviewed(all_gid_list)
reviewed_gid_list = ut.compress(all_gid_list, all_review_list)
reviewed_aid_list = ut.flatten(ibs.get_image_aids(reviewed_gid_list))
reviewed_pid_list = ut.flatten(ibs.get_annot_part_rowids(reviewed_aid_list))
reviewed_species_list = ibs.get_annot_species(reviewed_aid_list)
reviewed_viewpoint_list = ibs.get_annot_viewpoints(reviewed_aid_list)

species_list = [
    'right_whale_head',
]

viewpoint_mapping = {}

src_path = ibs.export_to_coco(species_list, species_mapping=species_mapping, viewpoint_mapping=viewpoint_mapping, include_parts=False, require_image_reviewed=True)
dst_path = '/data/public/datasets/orientation.rightwhale.coco'
ut.move(src_path, dst_path)

tar -zcvf orientation.hammerhead.coco.tar.gz orientation.hammerhead.coco/
tar -zcvf orientation.mantaray.coco.tar.gz   orientation.mantaray.coco/
tar -zcvf orientation.rightwhale.coco.tar.gz orientation.rightwhale.coco/
tar -zcvf orientation.seadragon.coco.tar.gz  orientation.seadragon.coco/
tar -zcvf orientation.seaturtle.coco.tar.gz  orientation.seaturtle.coco/

# rm -rf orientation.hammerhead.coco/
# rm -rf orientation.mantaray.coco/
# rm -rf orientation.rightwhale.coco/
# rm -rf orientation.seadragon.coco/
# rm -rf orientation.seaturtle.coco/
