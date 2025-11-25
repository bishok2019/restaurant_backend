import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import F

from apps.location.management.fixtures.load_fixtures import (
    DISTRICT_DATA_PATH,
    LOCAL_LEVEL_DATA_PATH,
    PROVINCE_DATA_PATH,
    WARD_DATA_PATH,
)
from apps.location.models import District, Palika, Province, Ward

province_csv_path = PROVINCE_DATA_PATH
district_csv_path = DISTRICT_DATA_PATH
local_level_csv_path = LOCAL_LEVEL_DATA_PATH
ward_count_csv_path = WARD_DATA_PATH


def create_province():
    province_df = pd.read_csv(province_csv_path)
    province_name_series = province_df["province_name"].replace(
        ["Province 1", "Province 2"], ["Koshi Province", "Madhesh Province"]
    )
    province_df["province_name"] = province_name_series

    final_province_df_ = province_df.rename(
        columns={"province_name": "name", "nepali_name": "nepali_name"}
    )
    final_province_df = final_province_df_
    df_data = [
        Province(
            province_id=row["province_id"],
            name=row["name"],
            nepali_name=row["nepali_name"],
        )
        for _, row in final_province_df.iterrows()
    ]
    province = Province.objects.bulk_create(df_data)
    return len(province)


def create_district():
    province_data = list(
        Province.objects.all().annotate(p_id=F("id")).values("p_id", "province_id")
    )
    province_df = pd.DataFrame(province_data)
    district_df = pd.read_csv(district_csv_path)

    final_district_df = district_df.rename(
        columns={"district_name": "name", "nepali_name": "nepali_name"}
    )

    ditsrict_merged_df = pd.merge(
        final_district_df,
        province_df[["province_id", "p_id"]],
        on="province_id",
        how="left",
    )

    df_data = [
        District(
            name=row["name"],
            nepali_name=row["nepali_name"],
            district_id=row["district_id"],
            province_id=row["p_id"],
        )
        for _, row in ditsrict_merged_df.iterrows()
    ]

    district = District.objects.bulk_create(df_data)
    return len(district)


def create_local_level():
    district_data = list(
        District.objects.all().annotate(d_id=F("id")).values("district_id", "d_id")
    )
    district_df = pd.DataFrame(district_data)

    local_level_df = pd.read_csv(local_level_csv_path)
    final_local_level_df = local_level_df.rename(
        columns={
            "local_level_name": "name",
            "local_level_id": "location_id",
            "nepali_name": "nepali_name",
        }
    )

    local_level_merged_df = pd.merge(
        final_local_level_df,
        district_df[["district_id", "d_id"]],
        on="district_id",
        how="left",
    )

    df_data = [
        Palika(
            name=row["name"],
            nepali_name=row["nepali_name"],
            location_id=row["location_id"],
            district_id=row["d_id"],
        )
        for _, row in local_level_merged_df.iterrows()
    ]
    location = Palika.objects.bulk_create(df_data)
    return len(location)


def create_ward_numbers():
    location_data = list(
        Palika.objects.all().annotate(l_id=F("id")).values("location_id", "l_id")
    )
    location_df = pd.DataFrame(location_data)

    ward_count_df = pd.read_csv(ward_count_csv_path)

    final_local_level_df = ward_count_df.rename(
        columns={"local_level_id": "location_id"}
    )

    ward_count_merged_df = pd.merge(
        final_local_level_df,
        location_df[["location_id", "l_id"]],
        on="location_id",
        how="left",
    )
    total_wards = 0

    for _, row in ward_count_merged_df.iterrows():
        data = [
            Ward(number=num, location_id=row["l_id"])
            for num in range(1, row["wards_count"] + 1)
        ]
        wards = Ward.objects.bulk_create(data)
        total_wards += len(wards)
    return total_wards


class Command(BaseCommand):
    def handle(self, *args, **options):
        # if Area.all_objects.all().count():
        #     Area.all_objects.all().delete()
        if Ward.all_objects.all().count():
            Ward.all_objects.all().delete()
        if Palika.all_objects.all().count():
            Palika.all_objects.all().delete()
        if District.all_objects.all().count():
            District.all_objects.all().delete()
        if Province.all_objects.all().count():
            Province.all_objects.all().delete()

        province = create_province()
        district = create_district()
        local_level = create_local_level()
        wards = create_ward_numbers()
        print(f"Total {province} provinces populated.")
        print(f"Total {district} districts populated.")
        print(f"Total {local_level} local levels populated.")
        print(f"Total {wards} wards populated.")
        print(f"{province + district + local_level + wards} rows affected in total.")
        return "Successfully loaded location data."
