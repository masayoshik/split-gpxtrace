#! /usr/bin/env python

import xml.etree.ElementTree as etree
import sys
MAXPT = 500

def main():
  if len(sys.argv) < 3:
    print('Usage %s <gpx file> <output file>' % sys.argv[0])
    sys.exit(1)

  try:
    tree = etree.parse(sys.argv[1])
  except:
    print 'Opening/parsing gpx file %s failed' % sys.argv[1]

  outfile = sys.argv[2]

  root = tree.getroot()

  gpx_ver=root.attrib['version']
  gpx_ver_major=int(gpx_ver.split(".")[0])
  gpx_ver_minor=int(gpx_ver.split(".")[1])
  gpxdef='http://www.topografix.com/GPX/%d/%d' % (gpx_ver_major, gpx_var_minor)
  etree.register_namespace("", '%s' % gpxdef)

  trk = root.findall('{%s}trk' % gpxdef)[0]
  trkseg = trk.findall('{%s}trkseg' % gpxdef)[0]
  name = trk.findall('{%s}name' % gpxdef)[0].text

  nr_pt = len(trkseg.getiterator('{%s}trkpt' % gpxdef))
  print 'GPX file contained %d track points' % nr_pt

  gpx = etree.Element('{%s}gpx'% gpxdef, attrib=root.attrib)
  # copy all tags except for <trk>..</trk>
  for i in root.getchildren():
    if i.tag != '{%s}trk' % gpxdef:
      gpx.append(i)

  # Split trk into multiple trk that has the max of MAXPT points
  for nf in range (0, nr_pt // MAXPT + 1):
    new_trk = etree.SubElement(root,'{%s}trk' % gpxdef)
    new_name = etree.SubElement(new_trk,'{%s}name' % gpxdef)
    new_name.text = '%s %03d' % (name, nf) 
    new_trkseg = etree.SubElement(new_trk,'{%s}trkseg' % gpxdef)

    st = nf * MAXPT
    en = (nf + 1) * MAXPT - 1
    if en > nr_pt:
      en = nr_pt

    for i in range(st, en):
      new_trkseg.append(trkseg.findall('{%s}trkpt' % gpxdef)[i])

    gpx.append(new_trk)

  with open(outfile, mode='wb') as f:
    f.write(etree.tostring(gpx))

if __name__ == '__main__':
  main()
