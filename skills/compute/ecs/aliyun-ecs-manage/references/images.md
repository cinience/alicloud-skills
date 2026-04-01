# ECS images

## Common operations

- Create/delete/modify: `CreateImage`, `DeleteImage`, `ModifyImageAttribute`
- Query: `DescribeImages`, `DescribeImageFromFamily`, `DescribeImageSupportInstanceTypes`
- Share: `DescribeImageSharePermission`, `ModifyImageSharePermission`
- Import/export/copy: `ImportImage`, `ExportImage`, `CopyImage`, `CancelCopyImage`

## Notes

- `CreateImage` creates a custom image from an instance or snapshot.
- Use `DescribeImages` to list public, custom, or shared images.

## References

- CreateImage: `https://www.alibabacloud.com/help/en/ecs/developer-reference/createimage`
- DescribeImages: `https://www.alibabacloud.com/help/id/ecs/developer-reference/describeimages`
