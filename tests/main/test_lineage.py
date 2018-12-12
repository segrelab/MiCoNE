"""
    Module containing tests for the lineage class
"""

import pytest

from mindpipe.main import Lineage


@pytest.mark.usefixtures("lineage_data")
class TestLineage:
    """ Tests for the Lineage class """

    def test_init(self, lineage_data):
        good_lineage = Lineage(**lineage_data["good"])
        assert good_lineage.Kingdom == lineage_data["good"]["Kingdom"]
        assert good_lineage.Phylum == lineage_data["good"]["Phylum"]
        assert good_lineage.Class == lineage_data["good"]["Class"]
        assert good_lineage.Order == lineage_data["good"]["Order"]
        assert good_lineage.Family == lineage_data["good"]["Family"]
        assert good_lineage.Genus == lineage_data["good"]["Genus"]
        assert good_lineage.Species == lineage_data["good"]["Species"]
        with pytest.raises(ValueError):
            Lineage(**lineage_data["bad"])

    def test_sub(self, lineage_data):
        lineage1 = Lineage(**lineage_data["good"])
        lineage2 = Lineage(**{**lineage_data["good"], **{"Order": "O2"}})
        assert lineage1 - lineage2 == lineage2 - lineage1
        common = {
            k: v
            for k, v in lineage_data["good"].items()
            if k in ["Kingdom", "Phylum", "Class"]
        }
        assert lineage1 - lineage2 == Lineage(**common)

    def test_name(self, lineage_data):
        lineage1 = Lineage(**lineage_data["good"])
        assert lineage1.name == ("Species", lineage_data["good"]["Species"])
        lineage2 = Lineage(**{**lineage_data["good"], **{"Genus": "", "Species": ""}})
        assert lineage2.name == ("Family", lineage_data["good"]["Family"])

    def test_str(self, lineage_data):
        lineage1 = Lineage(**lineage_data["good"])
        assert str(lineage1) == "k__Bacteria;p__P1;c__C1;o__O1;f__F1;g__G1;s__S1"
        lineage2 = Lineage(**{**lineage_data["good"], **{"Genus": "", "Species": ""}})
        assert str(lineage2) == "k__Bacteria;p__P1;c__C1;o__O1;f__F1;g__;s__"

    def test_from_str(self, lineage_data):
        lineage1 = Lineage(**lineage_data["good"])
        lineage2 = Lineage.from_str(str(lineage1))
        assert lineage1 == lineage2
        assert str(lineage1) == str(lineage2)

    def test_to_str(self, lineage_data):
        lineage1 = Lineage(**lineage_data["good"])
        assert (
            lineage1.to_str(style="gg", level="Family")
            == "k__Bacteria;p__P1;c__C1;o__O1;f__F1"
        )
        assert (
            lineage1.to_str(style="silva", level="Order")
            == "D_0__Bacteria;D_1__P1;D_2__C1;D_3__O1"
        )

    def test_to_dict(self, lineage_data):
        lineage1 = Lineage(**lineage_data["good"])
        assert lineage1.to_dict("Class") == {
            "Kingdom": "Bacteria",
            "Phylum": "P1",
            "Class": "C1",
        }

    def test_get_superset(self, lineage_data):
        lineage1 = Lineage(**lineage_data["good"])
        lineage2 = Lineage(**{**lineage_data["good"], **{"Genus": "", "Species": ""}})
        assert lineage1.get_superset("Family") == lineage2

    def test_taxid(self, lineage_data):
        lineage1 = Lineage.from_str(
            "k__Bacteria;p__Firmicutes;c__Clostridia;o__Clostridiales;f__Ruminococcaceae"
        )
        assert lineage1.taxid == 541_000
        lineage2 = Lineage.from_str(
            "k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enterobacterales;f__Enterobacteriaceae;g__Escherichia;s__coli"
        )
        assert lineage2.taxid == 562
        lineage3 = Lineage.from_str(
            "k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enterobacterales;f__Enterobacteriaceae;g__Escherichia;s__dragon"
        )
        with pytest.warns(UserWarning):
            assert lineage3.taxid == 561
