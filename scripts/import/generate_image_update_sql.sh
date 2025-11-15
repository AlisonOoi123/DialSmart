#!/bin/bash
# Generate SQL UPDATE statements to fix missing phone images

echo "-- SQL Script to Update Missing Phone Images"
echo "-- Generated from fyp_phoneDataset.csv"
echo ""
echo "SET SERVEROUTPUT ON;"
echo "SET FEEDBACK ON;"
echo ""

# Read CSV and generate UPDATE statements for phones with image URLs
awk -F',' '
BEGIN {
    print "DECLARE"
    print "  v_phone_id NUMBER;"
    print "  v_brand_id NUMBER;"
    print "  v_updated NUMBER := 0;"
    print "BEGIN"
}
NR > 1 {  # Skip header
    # Remove quotes and BOM
    gsub(/"/,"",$1); gsub(/"/,"",$2); gsub(/"/,"",$3);
    gsub(/\xEF\xBB\xBF/,"",$1);  # Remove BOM

    brand = $1
    model = $2
    image_url = $3

    # Only process if we have brand, model, and a valid image URL
    if (brand != "" && model != "" && image_url ~ /^https:\/\//) {
        # Escape single quotes in model name and URL
        gsub(/'\''/, "'\'''\''", model)
        gsub(/'\''/, "'\'''\''", image_url)

        print ""
        print "  -- Update: " brand " " model
        print "  SELECT id INTO v_brand_id FROM brands WHERE UPPER(name) = UPPER('\''" brand "'\'') AND ROWNUM = 1;"
        print "  "
        print "  SELECT id INTO v_phone_id"
        print "  FROM phones"
        print "  WHERE brand_id = v_brand_id"
        print "    AND UPPER(model_name) = UPPER('\''" model "'\'')"
        print "    AND (main_image IS NULL OR main_image = '\''N/A'\'' OR main_image = '\'''\'')"
        print "    AND ROWNUM = 1;"
        print "  "
        print "  IF v_phone_id IS NOT NULL THEN"
        print "    UPDATE phones"
        print "    SET main_image = '\''" image_url "'\''"
        print "    WHERE id = v_phone_id;"
        print "    v_updated := v_updated + 1;"
        print "  END IF;"
        print "  "
        print "  v_phone_id := NULL;"  # Reset for next iteration
        print "  v_brand_id := NULL;"
        print ""
        print "EXCEPTION"
        print "  WHEN NO_DATA_FOUND THEN NULL;"  # Skip if not found
        print "  WHEN OTHERS THEN NULL;"
    }
}
END {
    print ""
    print "  COMMIT;"
    print "  DBMS_OUTPUT.PUT_LINE('\''Updated '\'' || v_updated || '\'' phone images'\'');"
    print "END;"
    print "/"
}
' fyp_phoneDataset.csv

echo ""
echo "-- Verify the updates"
echo "SELECT b.name, COUNT(p.id) as phones_without_images"
echo "FROM phones p"
echo "JOIN brands b ON p.brand_id = b.id"
echo "WHERE (p.main_image IS NULL OR p.main_image = 'N/A' OR p.main_image = '')"
echo "GROUP BY b.name"
echo "ORDER BY phones_without_images DESC;"
