"""内容服务单元测试。"""

import pytest
from backend.app.services.content import (
    list_contents,
    get_content,
    create_content,
    update_content,
    delete_content,
    stream_url,
    scan_contents,
    search_contents,
    _contents,
    _next_id,
)


class TestContentService:
    """内容服务测试。"""

    @pytest.fixture(autouse=True)
    def reset_contents(self):
        """每个测试前重置内容存储。"""
        _contents.clear()
        _contents[1] = {
            "id": 1,
            "title": "Sample Track",
            "author": "Unknown Artist",
            "album": "Sample Album",
            "duration_seconds": 180,
            "size_bytes": 12345,
            "mime_type": "audio/mpeg",
            "folder_id": None,
            "content_metadata": {},
            "created_at": "2026-01-01T00:00:00",
            "updated_at": "2026-01-01T00:00:00",
        }
        yield
        _contents.clear()

    def test_list_contents_default(self):
        """测试默认列出内容。"""
        result = list_contents()
        
        assert "total" in result
        assert "items" in result
        assert result["total"] >= 1
        assert len(result["items"]) >= 1

    def test_list_contents_pagination(self):
        """测试内容分页。"""
        for i in range(5):
            create_content({"title": f"Track {i}", "duration_seconds": 100})
        
        result = list_contents(page=1, page_size=2)
        assert len(result["items"]) == 2
        assert result["total"] == 6

    def test_list_contents_sort_by_title(self):
        """测试按标题排序。"""
        create_content({"title": "AAA Track", "duration_seconds": 100})
        create_content({"title": "ZZZ Track", "duration_seconds": 100})
        
        result = list_contents(sort_by="title", order="asc")
        titles = [item["title"] for item in result["items"]]
        assert titles == sorted(titles)

    def test_list_contents_sort_desc(self):
        """测试降序排序。"""
        create_content({"title": "AAA Track", "duration_seconds": 100})
        create_content({"title": "ZZZ Track", "duration_seconds": 100})
        
        result = list_contents(sort_by="title", order="desc")
        titles = [item["title"] for item in result["items"]]
        assert titles == sorted(titles, reverse=True)

    def test_list_contents_filter_by_search(self):
        """测试通用搜索。"""
        create_content({"title": "Rock Album", "author": "Rock Band"})
        create_content({"title": "Jazz Album", "author": "Jazz Band"})
        
        result = list_contents(search="rock")
        assert result["total"] == 1
        assert result["items"][0]["title"] == "Rock Album"

    def test_list_contents_filter_by_author(self):
        """测试按作者筛选。"""
        create_content({"title": "Track 1", "author": "Author A"})
        create_content({"title": "Track 2", "author": "Author B"})
        
        result = list_contents(author="Author A")
        assert result["total"] == 1
        assert result["items"][0]["author"] == "Author A"

    def test_list_contents_filter_by_album(self):
        """测试按专辑筛选。"""
        create_content({"title": "Track 1", "album": "Album A"})
        create_content({"title": "Track 2", "album": "Album B"})
        
        result = list_contents(album="Album A")
        assert result["total"] == 1
        assert result["items"][0]["album"] == "Album A"

    def test_list_contents_filter_by_duration(self):
        """测试按时长筛选。"""
        create_content({"title": "Short", "duration_seconds": 60})
        create_content({"title": "Long", "duration_seconds": 300})
        
        result = list_contents(min_duration=100, max_duration=200)
        assert result["total"] == 1
        assert result["items"][0]["title"] == "Sample Track"

    def test_search_contents(self):
        """测试搜索内容。"""
        create_content({"title": "Rock Song", "author": "Rock Band"})
        
        result = search_contents("rock")
        assert result["total"] >= 1

    def test_search_contents_with_fields(self):
        """测试指定字段搜索。"""
        create_content({"title": "Rock Song", "author": "Jazz Band"})
        
        result = search_contents("rock", fields=["title"])
        assert result["total"] == 1

    def test_search_contents_no_match(self):
        """测试搜索无匹配结果。"""
        result = search_contents("nonexistent12345")
        assert result["total"] == 0

    def test_get_content_existing(self):
        """测试获取存在的内容。"""
        content = get_content(1)
        assert content is not None
        assert content["id"] == 1
        assert content["title"] == "Sample Track"

    def test_get_content_nonexistent(self):
        """测试获取不存在的内容。"""
        content = get_content(999)
        assert content is None

    def test_create_content_success(self):
        """测试成功创建内容。"""
        data = {
            "title": "New Track",
            "author": "New Artist",
            "duration_seconds": 200,
            "size_bytes": 50000,
            "mime_type": "audio/mpeg",
        }
        content = create_content(data)
        
        assert content["title"] == "New Track"
        assert content["author"] == "New Artist"
        assert content["duration_seconds"] == 200
        assert "id" in content
        assert "created_at" in content
        assert "updated_at" in content

    def test_create_content_minimal(self):
        """测试创建最小内容。"""
        data = {"title": "Minimal Track"}
        content = create_content(data)
        
        assert content["title"] == "Minimal Track"
        assert content["duration_seconds"] == 0
        assert content["size_bytes"] == 0

    def test_update_content_success(self):
        """测试成功更新内容。"""
        data = {"title": "Updated Title"}
        content = update_content(1, data)
        
        assert content is not None
        assert content["title"] == "Updated Title"

    def test_update_content_multiple_fields(self):
        """测试更新多个字段。"""
        data = {
            "title": "Updated Title",
            "duration_seconds": 300,
            "author": "Updated Author",
        }
        content = update_content(1, data)
        
        assert content["title"] == "Updated Title"
        assert content["duration_seconds"] == 300
        assert content["author"] == "Updated Author"

    def test_update_content_nonexistent(self):
        """测试更新不存在的内容。"""
        content = update_content(999, {"title": "New Title"})
        assert content is None

    def test_delete_content_success(self):
        """测试成功删除内容。"""
        result = delete_content(1)
        assert result is True
        assert get_content(1) is None

    def test_delete_content_nonexistent(self):
        """测试删除不存在的内容。"""
        result = delete_content(999)
        assert result is False

    def test_stream_url_existing(self):
        """测试获取存在的内容流URL。"""
        url = stream_url(1)
        assert url is not None
        assert "1" in url

    def test_stream_url_nonexistent(self):
        """测试获取不存在的内容流URL。"""
        url = stream_url(999)
        assert url is None

    def test_scan_contents(self):
        """测试扫描内容。"""
        result = scan_contents()
        assert "scanned" in result
        assert result["scanned"] is True
        assert "count" in result
        assert result["count"] >= 1
