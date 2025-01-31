#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

PKG_VERSION=""
SRC_TARBALL=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# parameters:
#
# --srcTarball  : src tarball file
#                 this file contains the 'initial' source code of the component
#                 and should be replaced with the new/modified src code
# --outFolder   : folder where to copy the new tarball(s)
# --pkgVersion  : package version
#
PARAMS=""
while (( "$#" )); do
    case "$1" in
        --srcTarball)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            SRC_TARBALL=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --outFolder)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            OUT_FOLDER=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --pkgVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            PKG_VERSION=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        -*|--*=) # unsupported flags
        echo "Error: Unsupported flag $1" >&2
        exit 1
        ;;
        *) # preserve positional arguments
        PARAMS="${PARAMS} $1"
        shift
        ;;
  esac
done

echo "--srcTarball   -> ${SRC_TARBALL}"
echo "--outFolder    -> ${OUT_FOLDER}"
echo "--pkgVersion   -> ${PKG_VERSION}"

if [ -z "${SRC_TARBALL}" ]; then
    echo "--srcTarball parameter cannot be empty"
    exit 1
fi

SRC_TARBALL=$(realpath "${SRC_TARBALL}")

if [ -z "${PKG_VERSION}" ]; then
    echo "--pkgVersion parameter cannot be empty"
    exit 1
fi

echo "-- create temp folder"
tmpdir=$(mktemp -d)
function cleanup {
    echo "+++ cleanup -> remove ${tmpdir}"
    rm -rf ${tmpdir}
}
trap cleanup EXIT

pushd "${tmpdir}" > /dev/null

echo "Unpacking source tarball..."
tar -xf "${SRC_TARBALL}"

cd "cert-manager-${PKG_VERSION}"

# We need to individually vendor each cmd we will build
vendor_directories=()

echo "Get vendored modules for each command"
for dir in cmd/*; do
    if [ -d "${dir}" ]; then
        echo "Vendoring '${dir}'"
        pushd "${dir}" > /dev/null
        go mod vendor
        vendor_directories+=("${dir}/vendor")
        popd > /dev/null
    fi
done

echo "Tar vendored modules"
VENDOR_TARBALL="${OUT_FOLDER}/cert-manager-${PKG_VERSION}-vendor.tar.gz"
tar  --sort=name \
     --mtime="2021-04-26 00:00Z" \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -cf "${VENDOR_TARBALL}" ${vendor_directories[@]}

popd > /dev/null
echo "cert-manager vendored modules are available at ${VENDOR_TARBALL}"
