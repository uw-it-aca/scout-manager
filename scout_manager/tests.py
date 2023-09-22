# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from scout_manager.test.pages_navigation import NavigationTests
from scout_manager.test.url_responses_test import urlStatusCheck
from scout_manager.test.dao.buildings import BuildingDaoTest
from scout_manager.test.dao.groups import GroupDaoTest
from scout_manager.test.dao.item import ItemDaoTest
from scout_manager.test.dao.spot import SpotDaoTest, BuildSpotJsonTest
from scout_manager.test.group_auth import GroupAuthTest
from scout_manager.test.api import ApiTest
from scout_manager.test.techloan.sync_techloan import SyncTechloanTest
