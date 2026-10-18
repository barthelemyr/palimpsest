# Data and third-party licences

The site embeds data derived from the sources below. Each remains under its own licence; this file gives the required attributions.

## Historical borders: Cliopatria
Bennett, J. S. et al. *Cliopatria*, version 0.2.1. Seshat Global History Databank. https://github.com/Seshat-Global-History-Databank/cliopatria
Licence: Creative Commons Attribution 4.0 International (CC BY 4.0).
Changes: projected to Equal Earth, simplified, converted to a shared-arc topology, hierarchy resolved, packed for the browser; overlaid on today's countries (computed links); population summed from HYDE inside each shape.

## Population: HYDE 3.3
Klein Goldewijk, K. et al. *History Database of the Global Environment (HYDE) 3.3*. Utrecht University, 2023. https://doi.org/10.24416/UU01-94FNH0
Licence: Creative Commons Attribution (the HYDE readme states CC BY 3.0; the data portal lists CC BY 4.0).
Used: country totals (`popc_c.txt`, base scenario) and population grids (`popc_<year>.asc`, base scenario) for 11 dates.
Changes: matched to Natural Earth countries; summed inside Cliopatria shapes; aggregated to 0.5° cells and divided by land area for the density layer.

## Coastlines and today's borders: Natural Earth
Natural Earth, 1:50m Admin 0 – Countries. https://www.naturalearthdata.com — Public domain.

## World Atlas TopoJSON
Mike Bostock, *world-atlas* 2.0.2 (derived from Natural Earth). https://github.com/topojson/world-atlas — ISC licence. Used for ISO numeric country codes.

## Flags: flag-icons
*flag-icons* 7.2.3 by Panayiotis Lipiridis and contributors. https://github.com/lipis/flag-icons — MIT licence. The flags were rasterised into one image embedded in the site. See the upstream LICENSE file for the full copyright notice, which applies to the flag images.

## Continents: countries-list
*countries-list* by Annexare Studio. https://github.com/annexare/Countries — MIT licence. See the upstream LICENSE file for the full copyright notice.

## Wikipedia
Articles are linked, not copied.

## Inspiration
ChartOrigin, *Timeline of World History* (poster). The selection of the original 21 columns follows the poster; all content was rewritten, corrected and extended, and no artwork is reused.

## This project's own data
The curated timeline dataset (`data/world_history_timeline_v4_5.json`) and the texts in the site: Creative Commons Attribution 4.0 International (CC BY 4.0). Please credit "Palimpsest (barthelemyr), made with Claude".
