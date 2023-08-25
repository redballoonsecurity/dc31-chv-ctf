from ofrak import *
from ofrak.core import *


async def main(ofrak_context: OFRAKContext, root_resource: Optional[Resource] = None):
    if root_resource is None:
        root_resource = await ofrak_context.create_root_resource_from_file("ivi.bin")

    await root_resource.unpack()

    genericbinary_0x0 = await root_resource.get_only_child(
        r_filter=ResourceFilter(
            tags={GenericBinary},
            attribute_filters=[
                ResourceAttributeValueFilter(attribute=Data.Offset, value=0)
            ],
        )
    )

    genericbinary_0x0.add_tag(Ihex)

    await genericbinary_0x0.save()

    await genericbinary_0x0.unpack()

    ihexprogram_0x0 = await genericbinary_0x0.get_only_child(
        r_filter=ResourceFilter(
            tags={IhexProgram},
            attribute_filters=[
                ResourceAttributeValueFilter(attribute=Data.Offset, value=0)
            ],
        )
    )

    await ihexprogram_0x0.run(GzipUnpacker, None)

    ihexprogram_0x0_genericbinary_0x0 = await ihexprogram_0x0.get_only_child(
        r_filter=ResourceFilter(
            tags={GenericBinary},
            attribute_filters=[
                ResourceAttributeValueFilter(attribute=Data.Offset, value=0)
            ],
        )
    )

    await ihexprogram_0x0_genericbinary_0x0.unpack()

    file_agl_ivi_demo_platform_html5_qemux86_64_ext4 = (
        await ihexprogram_0x0_genericbinary_0x0.get_only_child(
            r_filter=ResourceFilter(
                tags={File},
                attribute_filters=[
                    ResourceAttributeValueFilter(
                        attribute=AttributesType[FilesystemEntry].Name,
                        value="agl-ivi-demo-platform-html5-qemux86-64.ext4",
                    )
                ],
            )
        )
    )

    await file_agl_ivi_demo_platform_html5_qemux86_64_ext4.unpack()

    folder_etc = await file_agl_ivi_demo_platform_html5_qemux86_64_ext4.get_only_child(
        r_filter=ResourceFilter(
            tags={Folder},
            attribute_filters=[
                ResourceAttributeValueFilter(
                    attribute=AttributesType[FilesystemEntry].Name, value="etc"
                )
            ],
        )
    )

    folder_connman = await folder_etc.get_only_child(
        r_filter=ResourceFilter(
            tags={Folder},
            attribute_filters=[
                ResourceAttributeValueFilter(
                    attribute=AttributesType[FilesystemEntry].Name, value="connman"
                )
            ],
        )
    )

    file_flag1_txt = await folder_connman.get_only_child(
        r_filter=ResourceFilter(
            tags={File},
            attribute_filters=[
                ResourceAttributeValueFilter(
                    attribute=AttributesType[FilesystemEntry].Name, value="flag1.txt"
                )
            ],
        )
    )

    print((await file_flag1_txt.get_data()).decode("utf-8"))


if __name__ == "__main__":
    ofrak = OFRAK()
    if False:
        import ofrak_angr
        import ofrak_capstone

        ofrak.discover(ofrak_capstone)
        ofrak.discover(ofrak_angr)

    if False:
        import ofrak_binary_ninja
        import ofrak_capstone

        ofrak.discover(ofrak_capstone)
        ofrak.discover(ofrak_binary_ninja)

    if False:
        import ofrak_ghidra

        ofrak.discover(ofrak_ghidra)

    ofrak.run(main)
