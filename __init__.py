# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgissphericalstats
                                 A QGIS plugin
 qgissphericalstats
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-09-19
        copyright            : (C) 2022 by Juan M Haut
        email                : juanmariohaut@unex.es
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load qgissphericalstats class from file qgissphericalstats.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .qgissphericalstats import qgissphericalstats
    return qgissphericalstats(iface)
