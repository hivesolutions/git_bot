#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Git Bot
# Copyright (c) 2008-2019 Hive Solutions Lda.
#
# This file is part of Hive Git Bot.
#
# Hive Git Bot is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Git Bot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Git Bot. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os

import appier

from . import base

class Replica(base.GitBotBase):

    origin_url = appier.field(
        immutable = True,
        meta = "url",
        description = "Origin URL"
    )

    target_url = appier.field(
        immutable = True,
        meta = "url",
        description = "Origin URL"
    )

    branches = appier.field(
        type = list
    )

    @classmethod
    def validate(cls):
        return super(Replica, cls).validate() + [
            appier.not_null("origin_url"),
            appier.not_empty("origin_url"),
            appier.is_url("origin_url"),

            appier.not_null("target_url"),
            appier.not_empty("target_url"),
            appier.is_url("target_url"),

            appier.not_null("branches"),
            appier.not_empty("branches")
        ]

    def sync(self):
        is_new = not os.path.exists(self.repo_path)

        if not is_new:
            appier.Git.clone(self.origin_url, path = self.repo_path)

    @property
    def repo_path(self):
        base_path = appier.conf("REPOS_PATH", "repos")
        repo_path = os.path.join(base_path, self.repo_name)
        repo_path = os.path.abspath(repo_path)
        repo_path = os.path.normpath(repo_path)
        return repo_path

    @property
    def repo_name(self):
        origin_url_p = appier.legacy.urlparse(self.origin_url)
        basename = os.path.basename(origin_url_p.path)
        if basename.endswith(".git"): return basename[:-4]
        return basename
