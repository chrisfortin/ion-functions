#!/usr/bin/env python
"""
@package ion_functions.data.vel_functions
@file ion_functions/data/vel_functions.py
@author Stuart Pearce
@brief Module containing velocity family instrument related functions
"""

import numpy as np
import numexpr as ne

from ion_functions.data.generic_functions import magnetic_declination, magnetic_correction


def valid_lat(lat):
    """
    Checks if inputs are valid latitude values.
    """
    if isinstance(lat, np.ndarray):
        if np.any(lat > 90) or np.any(lat < -90):
            return False
        return True
    else:
        return -90 <= lat and lat <= 90


def valid_lon(lon):
    """
    Checks if inputs are valid longitude values.
    """
    if isinstance(lon, np.ndarray):
        if np.any(lon > 180) or np.any(lon < -180):
            return False
        return True
    else:
        return -180 <= lon and lon <= 180


# wrapper functions for use in ION
def nobska_mag_corr_east(u, v, lat, lon, timestamp, z=0):
    """
    Corrects the eastward velocity from a VEL3D-B Nobska MAVS 4
    instrument for magnetic declination to produce an L1 VELPTTU-VLE
    OOI data product.

    Given a velocity vector with components u & v in the magnetic East
    and magnetic North directions respectively, this function calculates
    the magnetic declination for the location, depth, and time of the
    vector from the World Magnetic Model (WMM) and transforms the vector
    to a true Earth reference frame.

    This function is a wrapper around the function "vel_mag_correction".

    Usage:

        u_cor = nobska_mag_corr_east(u, v, lat, lon, ntp_timestamp, z=0)

            where

        u_cor = eastward velocity, in true Earth frame, with the
            correction for magnetic declination applied. [m/s]

        u = uncorrected eastward velocity in magnetic Earth frame. [cm/s]
        v = uncorrected northward velocity in magnetic Earth frame. [cm/s]
        lat = latitude of the instrument [decimal degrees].  East is
            positive, West negative.
        lon = longitude of the instrument [decimal degrees]. North
            is positive, South negative.
        ntp_timestamp = NTP time stamp from a data particle
            [secs since 1900-01-01].
        z = depth of instrument relative to sea level [meters].
            Positive values only. Default value is 0.

    References:

        OOI (2012). Data Product Specification for Turbulent Point Water
            Velocity. Document Control Number 1341-00781.
            https://alfresco.oceanobservatories.org/ (See: Company Home
            >> OOI >> Controlled >> 1000 System Level >>
            1341-00781_Data_Product_SPEC_VELPTTU_Nobska_OOI.pdf)
    """
   # check for valid latitudes & longitudes; else return fill value
    if not valid_lat(lat) or not valid_lon(lon):
        return np.ones(u.shape, dtype=np.float) * -9999

    # correct for magnetic declination
    u_cor = vel_mag_correction(u, v, lat, lon, timestamp, z)[0]
    u_cor = ne.evaluate('u_cor / 100.')  # convert from cm/s to m/s

    # return true compass referenced East velocity in m/s
    return u_cor


def nobska_mag_corr_north(u, v, lat, lon, timestamp, z=0):
    """
    Corrects the northward velocity from a VEL3D-B Nobska MAVS 4
    instrument for magnetic declination to produce an L1 VELPTTU-VLN
    OOI data product.

    Given a velocity vector with components u & v in the magnetic East
    and magnetic North directions respectively, this function calculates
    the magnetic declination for the location, depth, and time of the
    vector from the World Magnetic Model (WMM) and transforms the vector
    to a true Earth reference frame.

    This function is a wrapper around the function "vel_mag_correction".

    Usage:

        v_cor = nobska_mag_corr_north(u, v, lat, lon, ntp_timestamp, z)

            where

        v_cor = northward velocity, in true Earth frame, with the
            correction for magnetic declination applied. [m/s]

        u = uncorrected eastward velocity in magnetic Earth frame. [cm/s]
        v = uncorrected northward velocity in magnetic Earth frame. [cm/s]
        lat = latitude of the instrument [decimal degrees].  East is
            positive, West negative.
        lon = longitude of the instrument [decimal degrees]. North
            is positive, South negative.
        ntp_timestamp = NTP time stamp from a data particle
            [secs since 1900-01-01].
        z = depth of instrument relative to sealevel [meters].
            Positive values only. Default value is 0.

    References:

        OOI (2012). Data Product Specification for Turbulent Point Water
            Velocity. Document Control Number 1341-00781.
            https://alfresco.oceanobservatories.org/ (See: Company Home
            >> OOI >> Controlled >> 1000 System Level >>
            1341-00781_Data_Product_SPEC_VELPTTU_Nobska_OOI.pdf)
    """
   # check for valid latitudes & longitudes; else return fill value
    if not valid_lat(lat) or not valid_lon(lon):
        return np.ones(u.shape, dtype=np.float) * -9999

    # correct for magnetic declination
    v_cor = vel_mag_correction(u, v, lat, lon, timestamp, z)[1]
    v_cor = ne.evaluate('v_cor / 100.')  # convert from cm/s to m/s

    # return true compass referenced North velocity in m/s
    return v_cor


# NOTE: It turns out all Nortek instruments output m/s rather than mm/s.
#   Thanks DPS authors!
def nortek_mag_corr_east(u, v, lat, lon, timestamp, z=0.0):
    """
    Corrects the eastward velocity from VEL3D-CD Nortek Vector, VEL3D-K
    Nortek Aquadopp II, or VELPT Nortek Aquadopp instruments for
    magnetic declination to produce an L1 VELPTTU-VLE or an L1
    VELPTMN-VLE OOI data product.

    Given a velocity vector with components u & v in the magnetic East
    and magnetic North directions respectively, this function calculates
    the magnetic declination for the location, depth, and time of the
    vector from the World Magnetic Model (WMM) and transforms the vector
    to a true Earth reference frame.

    This function is a wrapper around the function "vel_mag_correction".

    Usage:

        u_cor = nortek_mag_corr_east(u, v, lat, lon, ntp_timestamp, z)

            where

        u_cor = eastward velocity , in true Earth frame, with the
            correction for magnetic declination applied. [m/s]

        u = uncorrected eastward velocity in magnetic Earth frame. [m/s]
        v = uncorrected northward velocity in magnetic Earth frame. [m/s]
        lat = latitude of the instrument [decimal degrees].  East is
            positive, West negative.
        lon = longitude of the instrument [decimal degrees]. North
            is positive, South negative.
        ntp_timestamp = NTP time stamp from a data particle
            [secs since 1900-01-01].
        z = depth of instrument relative to sealevel [meters].
            Positive values only. Default value is 0.

    References:

        OOI (2012). Data Product Specification for Turbulent Point Water
            Velocity. Document Control Number 1341-00780.
            https://alfresco.oceanobservatories.org/ (See: Company Home
            >> OOI >> Controlled >> 1000 System Level >>
            1341-00780_Data_Product_SPEC_VELPTTU_Nortek_OOI.pdf)
    """
   # check for valid latitudes & longitudes; else return fill value
    if not valid_lat(lat) or not valid_lon(lon):
        return np.ones(u.shape, dtype=np.float) * -9999

    # correct for magnetic declination
    u_cor = vel_mag_correction(u, v, lat, lon, timestamp, z)[0]
    #u_cor = ne.evaluate('u_cor / 1000.')  # convert from mms/ to m/s

    # return true compass referenced East velocity in m/s
    return u_cor


def nortek_mag_corr_north(u, v, lat, lon, timestamp, z=0.0):
    """
    Corrects the northward velocity from VEL3D-CD Nortek Vector, VEL3D-K
    Nortek Aquadopp II, and VELPT Nortek Aquadopp instruments for
    magnetic declination to produce an L1 VELPTTU-VLN or an L1
    VELPTMN-VLN OOI data product.

    Given a velocity vector with components u & v in the magnetic East
    and magnetic North directions respectively, this function calculates
    the magnetic declination for the location, depth, and time of the
    vector from the World Magnetic Model (WMM) and transforms the vector
    to a true Earth reference frame.

    This function is a wrapper around the function "vel_mag_correction".

    Usage:

        v_cor = nortek_mag_corr_north(u, v, lat, lon, ntp_timestamp, z)

            where

        v_cor = northward velocity, in true Earth frame, with the
            correction for magnetic declination applied. [m/s]

        u = uncorrected eastward velocity in magnetic Earth frame. [m/s]
        v = uncorrected northward velocity in magnetic Earth frame. [m/s]
        lat = latitude of the instrument [decimal degrees].  East is
            positive, West negative.
        lon = longitude of the instrument [decimal degrees]. North
            is positive, South negative.
        ntp_timestamp = NTP time stamp from a data particle
            [secs since 1900-01-01].
        z = depth of instrument relative to sealevel [meters].
            Positive values only. Default value is 0.

    References:

        OOI (2012). Data Product Specification for Turbulent Point Water
            Velocity. Document Control Number 1341-00780.
            https://alfresco.oceanobservatories.org/ (See: Company Home
            >> OOI >> Controlled >> 1000 System Level >>
            1341-00780_Data_Product_SPEC_VELPTTU_Nortek_OOI.pdf)
    """
   # check for valid latitudes & longitudes; else return fill value
    if not valid_lat(lat) or not valid_lon(lon):
        return np.ones(u.shape, dtype=np.float) * -9999

    # correct for magnetic declination
    v_cor = vel_mag_correction(u, v, lat, lon, timestamp, z)[1]
    #v_cor = ne.evaluate('v_cor/1000.')  # convert from mms/ to m/s

    # return true compass referenced North velocity in m/s
    return v_cor

## See NOTE above nortek_mag_correction
#def aquadopp2_mag_corr_east(u, v, lat, lon, timestamp, z=0.0):
#    """
#    Corrects the eastward velocity from VEL3D-K Nortek Aquadopp II for
#    magnetic declination to produce an L1 VELPTTU-VLE OOI data product.
#
#    Given a velocity vector with components u & v in the magnetic East
#    and magnetic North directions respectively, this function calculates
#    the magnetic declination for the location, depth, and time of the
#    vector from the World Magnetic Model (WMM) and transforms the vector
#    to a true Earth reference frame.
#
#    This function is a wrapper around the function "vel_mag_correction".
#
#    Usage:
#
#        u_cor = aquadopp2_mag_corr_east(u, v, lat, lon, ntp_timestamp, z)
#
#            where
#
#        u_cor = eastward velocity , in true Earth frame, with the
#            correction for magnetic declination applied. [m/s]
#
#        u = uncorrected eastward velocity in magnetic Earth frame. [m/s]
#        v = uncorrected northward velocity in magnetic Earth frame. [m/s]
#        lat = latitude of the instrument [decimal degrees].  East is
#            positive, West negative.
#        lon = longitude of the instrument [decimal degrees]. North
#            is positive, South negative.
#        ntp_timestamp = NTP time stamp from a data particle
#            [secs since 1900-01-01].
#        z = depth of instrument relative to sealevel [meters].
#            Positive values only. Default value is 0.
#
#    References:
#
#        OOI (2012). Data Product Specification for Turbulent Point Water
#            Velocity. Document Control Number 1341-00780.
#            https://alfresco.oceanobservatories.org/ (See: Company Home
#            >> OOI >> Controlled >> 1000 System Level >>
#            1341-00780_Data_Product_SPEC_VELPTTU_Nortek_OOI.pdf)
#    """
#   # check for valid latitudes & longitudes; else return fill value
#    if not valid_lat(lat) or not valid_lon(lon):
#        return np.ones(u.shape, dtype=np.float) * -9999
#
#    # correct for magnetic declination
#    u_cor = vel_mag_correction(u, v, lat, lon, timestamp, z)[0]
#
#    return v_cor  # return true compass referenced East velocity in m/s
#
#
#def aquadopp2_mag_corr_north(u, v, lat, lon, timestamp, z=0.0):
#    """
#    Corrects the northward velocity from VEL3D-K Nortek Aquadopp II for
#    magnetic declination to produce an L1 VELPTTU-VLN OOI data product.
#
#    Given a velocity vector with components u & v in the magnetic East
#    and magnetic North directions respectively, this function calculates
#    the magnetic declination for the location, depth, and time of the
#    vector from the World Magnetic Model (WMM) and transforms the vector
#    to a true Earth reference frame.
#
#    This function is a wrapper around the function "vel_mag_correction".
#
#    Usage:
#
#        v_cor = aquadopp2_mag_corr_north(u, v, lat, lon, ntp_timestamp, z)
#
#            where
#
#        v_cor = northward velocity, in true Earth frame, with the
#            correction for magnetic declination applied. [m/s]
#
#        u = uncorrected eastward velocity in magnetic Earth frame. [m/s]
#        v = uncorrected northward velocity in magnetic Earth frame. [m/s]
#        lat = latitude of the instrument [decimal degrees].  East is
#            positive, West negative.
#        lon = longitude of the instrument [decimal degrees]. North
#            is positive, South negative.
#        ntp_timestamp = NTP time stamp from a data particle
#            [secs since 1900-01-01].
#        z = depth of instrument relative to sealevel [meters].
#            Positive values only. Default value is 0.
#
#    References:
#
#        OOI (2012). Data Product Specification for Turbulent Point Water
#            Velocity. Document Control Number 1341-00780.
#            https://alfresco.oceanobservatories.org/ (See: Company Home
#            >> OOI >> Controlled >> 1000 System Level >>
#            1341-00780_Data_Product_SPEC_VELPTTU_Nortek_OOI.pdf)
#    """
#   # check for valid latitudes & longitudes; else return fill value
#    if not valid_lat(lat) or not valid_lon(lon):
#        return np.ones(u.shape, dtype=np.float) * -9999
#
#    # correct for magnetic declination
#    v_cor = vel_mag_correction(u, v, lat, lon, timestamp, z)[1]
#
#    # return true compass referenced North velocity in m/s
#    return v_cor


# major function
def vel_mag_correction(u, v, lat, lon, ntp_timestamp, z=0.0, zflag=-1):
    """
    Description:

        Given a velocity vector U, measured in a sensor frame that is
        referenced to Earth's magnetic field, with components u & v in
        the magnetic East and magnetic North directions respectively;
        vel_mag_correction transforms U to true Earth referenced
        directions by a rotation that removes the magnetic declination.
        Magnetic Declination, theta(x,y,z,t), is the azimuthal angular
        offset between true North and magnetic North as a function of
        Earth referenced location (latitude, longitude, & height/depth)
        and time. Magnetic declination is estimated from the World
        Magnetic Model (WMM) using the location and time of the vector.

    Usage:

        u_cor, v_cor = vel_mag_correction(u, v, lat, lon, ntp_timestamp, z, zflag)

            where

        u_cor = eastward velocity, in true Earth frame, with the
            correction for magnetic declination applied.
        v_cor = northward velocity, in true Earth frame, with the
            correction for magnetic declination applied.

        u = uncorrected eastward velocity in magnetic Earth frame.
        v = uncorrected northward velocity in magnetic Earth frame.
        lat = latitude of the instrument [decimal degrees].  East is
            positive, West negative.
        lon = longitude of the instrument [decimal degrees]. North
            is positive, South negative.
        ntp_timestamp = NTP time stamp from a data particle
            [secs since 1900-01-01].
        z = depth or height of instrument relative to sealevel [meters].
            Positive values only. Default value is 0.
        zflag = indicates whether to use z as a depth or height relative
            to sealevel. -1=depth (i.e. -z) and 1=height (i.e. +z). -1
            is the default, because Oceanography!

    Implemented by:

        2013-04-17: Stuart Pearce. Initial code.
        2013-04-24: Stuart Pearce. Changed to be general for all velocity
                    instruments.
        2014-02-05: Christopher Wingard. Edited to use magnetic corrections in
                    the generic_functions module.

    References:

        OOI (2012). Data Product Specification for Turbulent Point Water
            Velocity. Document Control Number 1341-00781.
            https://alfresco.oceanobservatories.org/ (See: Company Home
            >> OOI >> Controlled >> 1000 System Level >>
            1341-00781_Data_Product_SPEC_VELPTTU_Nobska_OOI.pdf)

        OOI (2012). Data Product Specification for Turbulent Point Water
            Velocity. Document Control Number 1341-00780.
            https://alfresco.oceanobservatories.org/ (See: Company Home
            >> OOI >> Controlled >> 1000 System Level >>
            1341-00780_Data_Product_SPEC_VELPTTU_Nortek_OOI.pdf)
    """
    # retrieve the magnetic declination
    theta = magnetic_declination(lat, lon, ntp_timestamp, z, zflag)

    # apply the magnetic declination correction
    magvar = np.vectorize(magnetic_correction)
    u_cor, v_cor = magvar(theta, u, v)

    return u_cor, v_cor
