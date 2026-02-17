from django.db import models

class ParcelCache(models.Model):
    pnu = models.CharField(max_length=19, unique=True, db_index=True)
    geometry_data = models.JSONField(help_text="GeoJSON geometry data")
    address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pnu} ({self.address})"

    class Meta:
        db_table = 'parcel_cache'
        verbose_name = '지적경계 캐시'
        verbose_name_plural = '지적경계 캐시'


class LandInfoCache(models.Model):
    """토지 및 건축물 정보 캐시"""
    pnu = models.CharField(max_length=19, unique=True, db_index=True)
    data = models.JSONField(help_text="Land and building information")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Land Info: {self.pnu}"

    class Meta:
        db_table = 'land_info_cache'
        verbose_name = '토지정보 캐시'
        verbose_name_plural = '토지정보 캐시'


class WFSCache(models.Model):
    """V-World WFS 데이터 캐시"""
    cache_key = models.CharField(max_length=255, unique=True, db_index=True)
    data = models.JSONField(help_text="Layer GeoJSON data")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wfs_cache'
        verbose_name = 'WFS 경계 캐시'
        verbose_name_plural = 'WFS 경계 캐시'


class KamcoCache(models.Model):
    """한국자산관리공사 온비드 공매물건 캐시"""
    cache_key = models.CharField(max_length=255, unique=True, db_index=True)
    data = models.JSONField(help_text="Kamco items JSON data")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'kamco_cache'
        verbose_name = '공매물건 캐시'
        verbose_name_plural = '공매물건 캐시'


class WarehouseCache(models.Model):
    """경기도 물류창고 데이터 캐시"""
    cache_key = models.CharField(max_length=255, unique=True, db_index=True)
    data = models.JSONField(help_text="Warehouse items JSON data")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'warehouse_cache'
        verbose_name = '물류창고 캐시'
        verbose_name_plural = '물류창고 캐시'


class HospitalCache(models.Model):
    """보건복지부 병의원 병상수 데이터 캐시"""
    cache_key = models.CharField(max_length=255, unique=True, db_index=True)
    data = models.JSONField(help_text="Hospital statistics JSON data")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hospital Cache: {self.cache_key}"

    class Meta:
        db_table = 'hospital_cache'
        verbose_name = '병상수 캐시'
        verbose_name_plural = '병상수 캐시'
