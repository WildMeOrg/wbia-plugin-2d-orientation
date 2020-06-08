import wbia
import random
import numpy as np
import vtool as vt
import utool as ut
import yaml
import uuid

'''
databases
  - sea turtles
  - sea dragons
  - mantas
  - hammerheads
  - right whale heads
  - [SKIPPED] spotted dolphin dorsal fins
'''

MIN_ROWIDS = 2
MAX_ROWIDS = 5
MIN_DELTA = 60 * 60 * 6


TEST_URLS = {
    'hammerhead' : 'https://cthulhu.dyn.wildme.io/public/datasets/orientation.hammerhead.coco.test.json',
    'mantaray'   : 'https://cthulhu.dyn.wildme.io/public/datasets/orientation.mantaray.coco.test.json',
    'rightwhale' : 'https://cthulhu.dyn.wildme.io/public/datasets/orientation.rightwhale.coco.test.json',
    'seadragon'  : 'https://cthulhu.dyn.wildme.io/public/datasets/orientation.seadragon.coco.test.json',
    'seaturtle'  : 'https://cthulhu.dyn.wildme.io/public/datasets/orientation.seaturtle.coco.test.json',
}


def encounter_deltas(unixtimes):
    assert None not in unixtimes
    assert -1 not in unixtimes
    previous = 0
    delta_list = []
    for unixtime in unixtimes + [None]:
        if unixtime is None:
            break
        else:
            try:
                delta = unixtime - previous
            except Exception:
                delta = 0
        # print(delta)
        assert delta >= 0
        delta_list.append(delta)
        previous = unixtime
    assert len(delta_list) == len(unixtimes)
    delta_list = np.array(delta_list)
    return delta_list


def align(bbox, theta, width, height):
    # Transformation matrix
    R = vt.rotation_around_bbox_mat3x3(theta, bbox)
    # Get verticies of the annotation polygon
    verts = vt.verts_from_bbox(bbox, close=True)
    # Rotate and transform vertices
    xyz_pts = vt.add_homogenous_coordinate(np.array(verts).T)
    trans_pts = vt.remove_homogenous_coordinate(R.dot(xyz_pts))
    new_verts = np.round(trans_pts).astype(np.int).T.tolist()
    x_points = [pt[0] for pt in new_verts]
    y_points = [pt[1] for pt in new_verts]
    xmin = int(min(x_points))
    xmax = int(max(x_points))
    ymin = int(min(y_points))
    ymax = int(max(y_points))
    # Bounds check
    xmin = max(xmin, 0)
    ymin = max(ymin, 0)
    xmax = min(xmax, width - 1)
    ymax = min(ymax, height - 1)
    xtl = xmin
    ytl = ymin
    w = xmax - xmin
    h = ymax - ymin
    return (xtl, ytl, w, h, )


test_uuid_list = []
for model_tag in TEST_URLS:
    json_url = TEST_URLS[model_tag]
    json_filepath = ut.grab_file_url(json_url, appname='wbia_2d_orientation', check_hash=False)

    with open(json_filepath, 'r') as file:
        json_data = yaml.load(file, Loader=yaml.FullLoader)
        annotation_data = json_data['annotations']
        test_uuid_list_ = ut.take_column(annotation_data, 'uuid')
        print(len(set(test_uuid_list_)))
        test_uuid_list += test_uuid_list_
assert len(test_uuid_list) == len(set(test_uuid_list))
test_uuid_list = [uuid.UUID(test_uuid) for test_uuid in test_uuid_list]
test_uuid_set = set(test_uuid_list)

################################################################################

desired_species_list = [
    'turtle_green',
    'turtle_hawksbill',
    'turtle_oliveridley',
    'seadragon_leafy',
    'seadragon_weedy',
    'manta_ray_giant',
    'shark_hammerhead',
    'right_whale_head',
]

species_mapping = {
    'manta_ray': 'manta_ray_giant',
}

viewpoint_mapping = {}
for species in desired_species_list:
    if species in ['turtle_green', 'turtle_hawksbill', 'turtle_oliveridley', 'seadragon_leafy', 'seadragon_weedy']:
        viewpoint_mapping[species] = {
            'frontleft'  : 'left',
            'left'       : 'left',
            'backleft'   : 'left',
            'upleft'     : 'left',
            'downleft'   : 'left',
            'frontright' : 'right',
            'right'      : 'right',
            'backright'  : 'right',
            'upright'    : 'right',
            'downright'  : 'right',
        }
    elif species in ['manta_ray_giant']:
        viewpoint_mapping[species] = {
            None         : 'down',
        }
    elif species in ['right_whale_head']:
        viewpoint_mapping[species] = {
            'up'         : 'up',
        }
    else:
        viewpoint_mapping[species] = {}

db_value_list = [
    ('/data/wbia/ST_Master', 'left', True,  False, True ),
    ('/data/wbia/SD_Master', 'left', True,  False, True ),
    ('/data/wbia/MM_Master', 'down', False, False, False),
    ('/data/wbia/HH_Master', None,   False, False, True ),
    ('/data/wbia/RW_Master', 'up',   False, True,  True ),
]

ibs_dst = wbia.opendb(dbdir='/data/wbia/testdb_orientation_updated/')

for dbdir, desired_viewpoint, use_parts, reviewed_only, test_only in db_value_list:

    ibs_src = wbia.opendb(dbdir=dbdir)
    print(ibs_src)

    test_only = False

    if reviewed_only:
        all_gid_list = ibs_src.get_valid_gids()
        all_review_list = ibs_src.get_image_reviewed(all_gid_list)
        reviewed_gid_list = ut.compress(all_gid_list, all_review_list)
        reviewed_aid_list = ut.flatten(ibs_src.get_image_aids(reviewed_gid_list))
        candidate_aid_list = reviewed_aid_list
    else:
        all_aid_list = ibs_src.get_valid_aids()
        candidate_aid_list = all_aid_list

    candidate_uuid_list = ibs_src.get_annot_uuids(candidate_aid_list)
    candidate_nid_list = ibs_src.get_annot_nids(candidate_aid_list)
    candidate_species_list = ibs_src.get_annot_species(candidate_aid_list)
    candidate_viewpoint_list = ibs_src.get_annot_viewpoints(candidate_aid_list)
    candidate_pids_list = ibs_src.get_annot_part_rowids(candidate_aid_list)
    candidate_part_types_list = list(map(ibs_src.get_part_types, candidate_pids_list))

    nid_dict = {}
    zipped = list(zip(
        candidate_aid_list,
        candidate_uuid_list,
        candidate_nid_list,
        candidate_species_list,
        candidate_viewpoint_list,
        candidate_pids_list,
        candidate_part_types_list,
    ))
    c0, c1, c2, c3, c4, c5, c6 = 0, 0, 0, 0, 0, 0, 0
    for aid, uuid_, nid, species, viewpoint, pid_list, type_list in zipped:
        c0 += 1
        if nid <= 0:
            c1 += 1
            continue
        if test_only:
            if uuid_ not in test_uuid_set:
                c2 += 1
                continue

        if use_parts:
            if len(pid_list) != 1:
                c3 += 1
                continue
            pid = pid_list[0]
            type_ = type_list[0]
            if type_ not in ['head']:
                c3 += 1
                continue

        species   = species_mapping.get(species, species)
        viewpoint = viewpoint_mapping.get(species, {}).get(viewpoint, None)

        if species not in desired_species_list:
            c4 += 1
            continue
        if viewpoint is None:
            c4 += 1
            continue
        if viewpoint != desired_viewpoint:
            c4 += 1
            continue

        c5 += 1

        if species not in nid_dict:
            nid_dict[species] = {}
        if viewpoint not in nid_dict[species]:
            nid_dict[species][viewpoint] = {}
        if nid not in nid_dict[species][viewpoint]:
            nid_dict[species][viewpoint][nid] = []

        rowid = pid if use_parts else aid
        nid_dict[species][viewpoint][nid].append(rowid)

    keep_dict = {}
    for species in nid_dict:
        for viewpoint in nid_dict[species]:
            for nid in nid_dict[species][viewpoint]:
                rowid_list = nid_dict[species][viewpoint][nid]

                if use_parts:
                    pid_list = rowid_list
                    aid_list = ibs_src.get_part_aids(pid_list)
                else:
                    aid_list = rowid_list

                unixtime_list = ibs_src.get_annot_image_unixtimes(aid_list)

                valid_list = list(np.array(unixtime_list) >= 0)
                aid_list = ut.compress(aid_list, valid_list)
                unixtime_list = ut.compress(unixtime_list, valid_list)

                values = sorted(zip(unixtime_list, rowid_list))
                unixtime_list = ut.take_column(values, 0)
                rowid_list = ut.take_column(values, 1)

                # print('\nStarting with:\n\tRowids:  %r\n\tTimes: %r' % (rowid_list, unixtime_list))

                delta_list = encounter_deltas(unixtime_list)
                candidate_list = delta_list < MIN_DELTA
                while True in candidate_list:
                    candidate_index = np.argmin(delta_list)
                    # print('Popping index %d' % (candidate_index, ))
                    unixtime_list.pop(candidate_index)
                    rowid_list.pop(candidate_index)
                    delta_list = encounter_deltas(unixtime_list)
                    candidate_list = delta_list < MIN_DELTA

                # print('Ended with:\n\tRowids:  %r\n\tTimes: %r' % (rowid_list, unixtime_list))

                rowid_list = list(set(rowid_list))
                if len(rowid_list) >= MIN_ROWIDS:
                    random.shuffle(rowid_list)
                    max_rowids = min(len(rowid_list), MAX_ROWIDS)
                    keep_rowid_list = rowid_list[:max_rowids]
                else:
                    keep_rowid_list = []

                if len(keep_rowid_list) > 0:
                    if species not in keep_dict:
                        keep_dict[species] = {}
                    if viewpoint not in keep_dict[species]:
                        keep_dict[species][viewpoint] = {
                            'aids': [],
                            'pids': [],
                            'nids': [],
                        }
                    keep_dict[species][viewpoint]['nids'] += [nid]
                    key = 'pids' if use_parts else 'aids'
                    keep_dict[species][viewpoint][key] += keep_rowid_list
                    c6 += len(keep_rowid_list)

    # print(set(candidate_species_list))
    print(c0, c1, c2, c3, c4, c5, c6)
    # print(set(ut.flatten(candidate_part_types_list)))

    for species in keep_dict:
        for viewpoint in keep_dict[species]:
            aids = keep_dict[species][viewpoint]['aids']
            pids = keep_dict[species][viewpoint]['pids']
            nids = keep_dict[species][viewpoint]['nids']
            print(species, viewpoint, len(aids), len(pids), len(nids), )

            gid_list       = []
            bbox_list      = []
            theta_list     = []
            species_list   = []
            viewpoint_list = []
            name_list      = []
            note_list      = []

            for aid in aids:
                gid       = ibs_src.get_annot_gids(aid)
                bbox      = ibs_src.get_annot_bboxes(aid)
                theta     = ibs_src.get_annot_thetas(aid)
                species   = ibs_src.get_annot_species(aid)
                viewpoint = ibs_src.get_annot_viewpoints(aid)
                name      = ibs_src.get_annot_names(aid)

                species   = species_mapping.get(species, species)
                viewpoint = viewpoint_mapping.get(species, {}).get(viewpoint, None)

                gid_list       += [gid]
                bbox_list      += [bbox]
                theta_list     += [theta]
                species_list   += [species]
                viewpoint_list += [viewpoint]
                name_list      += [name]
                note_list      += ['source']

            for pid in pids:
                aid       = ibs_src.get_part_aids(pid)
                gid       = ibs_src.get_annot_gids(aid)
                bbox      = ibs_src.get_part_bboxes(pid)
                theta     = ibs_src.get_part_thetas(pid)
                species   = ibs_src.get_annot_species(aid)
                type_     = ibs_src.get_part_types(pid)
                viewpoint = ibs_src.get_annot_viewpoints(aid)
                name      = ibs_src.get_annot_names(aid)

                species   = species_mapping.get(species, species)
                species   = '%s+%s' % (species, type_, )
                viewpoint = viewpoint_mapping.get(species, {}).get(viewpoint, None)

                gid_list       += [gid]
                bbox_list      += [bbox]
                theta_list     += [theta]
                species_list   += [species]
                viewpoint_list += [viewpoint]
                name_list      += [name]
                note_list      += ['source']

            # align(bbox, theta, width, height)

            gpath_list = ibs_src.get_image_paths(gid_list)
            size_list  = ibs_src.get_image_sizes(gid_list)

            gids_ = ibs_dst.add_images(gpath_list, ensure_loadable=False, ensure_exif=False)
            assert None not in gids_

            # Source
            ibs_dst.add_annots(
                gids_,
                bbox_list=bbox_list,
                theta_list=theta_list,
                species_list=species_list,
                viewpoint_list=viewpoint_list,
                name_list=name_list,
                notes_list=note_list
            )

            # Aligned
            bbox_list_  = []
            theta_list_ = []
            note_list_  = []
            for bbox, theta, size in zip(bbox_list, theta_list, size_list):
                width, height = size
                bbox_ = align(bbox, theta, width, height)
                bbox_list_.append(bbox_)
                theta_list_.append(1e-3)
                note_list_.append('aligned')

            ibs_dst.add_annots(
                gids_,
                bbox_list=bbox_list_,
                theta_list=theta_list_,
                species_list=species_list,
                viewpoint_list=viewpoint_list,
                name_list=name_list,
                notes_list=note_list_
            )

            previous_bbox_list_  = bbox_list_
            previous_theta_list_ = theta_list_

            # Squared
            bbox_list_  = []
            theta_list_ = []
            note_list_  = []
            for bbox, theta in zip(previous_bbox_list_, previous_theta_list_):
                xtl, ytl, w, h = bbox
                centerx = xtl + w // 2
                centery = ytl + h // 2
                radius = max(w // 2, h // 2)
                xtl_ = centerx - radius
                ytl_ = centery - radius
                w_ = radius * 2
                h_ = radius * 2
                bbox_ = (xtl_, ytl_, w_, h_, )
                bbox_list_.append(bbox_)
                theta_list_.append(-1e-3)
                note_list_.append('squared')

            ibs_dst.add_annots(
                gids_,
                bbox_list=bbox_list_,
                theta_list=theta_list_,
                species_list=species_list,
                viewpoint_list=viewpoint_list,
                name_list=name_list,
                notes_list=note_list_
            )

            previous_bbox_list_  = bbox_list_
            previous_theta_list_ = theta_list_

            gid_list_       = []
            bbox_list_      = []
            theta_list_     = []
            species_list_   = []
            viewpoint_list_ = []
            name_list_      = []
            note_list_      = []
            zipped = list(zip(
                gids_,
                previous_bbox_list_,   # Re-use the aligned box and theta from before
                previous_theta_list_,  # Re-use the aligned box and theta from before
                size_list,
                species_list,
                viewpoint_list,
                name_list,
            ))
            for gid, bbox, theta, size, species, viewpoint, name in zipped:
                existing_note_list = ibs_src.get_annot_notes(ibs_src.get_image_aids(gid))

                for index in range(10):
                    note_ = 'random-%02d' % (index + 1, )
                    if note_ in existing_note_list:
                        continue
                    width, height = size
                    theta_ = random.uniform(0.0, 2.0 * np.pi)
                    # bbox_ = align(bbox, theta_, width, height)
                    gid_list_.append(gid)
                    bbox_list_.append(bbox)
                    theta_list_.append(theta_)
                    species_list_.append(species)
                    viewpoint_list_.append(viewpoint)
                    name_list_.append(name)
                    note_list_.append(note_)

            ibs_dst.add_annots(
                gid_list_,
                bbox_list=bbox_list_,
                theta_list=theta_list_,
                species_list=species_list_,
                viewpoint_list=viewpoint_list_,
                name_list=name_list_,
                notes_list=note_list_
            )
