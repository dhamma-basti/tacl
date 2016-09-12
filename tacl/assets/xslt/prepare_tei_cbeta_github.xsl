<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
                xmlns:cb="http://www.cbeta.org/ns/1.0"
                xmlns:tei="http://www.tei-c.org/ns/1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output encoding="UTF-8" method="xml" />

  <xsl:strip-space elements="*" />

  <xsl:key name="anchored" match="tei:note[@target]"
           use="substring-after(@target, '#')" />

  <xsl:key name="anchored_start" match="*[@from]"
           use="substring-after(@from, '#')" />

  <xsl:template match="tei:anchor">
    <xsl:apply-templates select="key('anchored', @xml:id)" />
    <xsl:apply-templates select="key('anchored_start', @xml:id)" />
  </xsl:template>

  <xsl:template match="tei:app/@from" />
  <xsl:template match="tei:app/@to" />

  <xsl:template match="tei:back" />

  <xsl:template match="tei:charDecl" />

  <!-- Handling of characters not in Unicode. -->
  <xsl:template match="tei:g[@ref]" priority="10">
    <xsl:apply-templates select="id(substring-after(@ref, '#'))"
                         mode="nonunicode" />
  </xsl:template>

  <xsl:template match="tei:char" mode="nonunicode">
    <xsl:choose>
      <xsl:when test="tei:charProp/tei:localName='composition'">
        <xsl:value-of select="tei:charProp[tei:localName='composition']/tei:value" />
      </xsl:when>
      <xsl:when test="tei:charProp/tei:localName='Romanized form in Unicode transcription'">
        <xsl:value-of select="tei:charProp[tei:localName='Romanized form in Unicode transcription']/tei:value" />
      </xsl:when>
      <xsl:when test="tei:charProp/tei:localName='Character in the Siddham font'">
        <xsl:value-of select="tei:charProp[tei:localName='Character in the Siddham font']/tei:value" />
      </xsl:when>
      <xsl:when test="tei:charProp/tei:localName='rjchar'">
        <xsl:value-of select="tei:charProp[tei:localName='rjchar']/tei:value" />
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>GAIJI WITHOUT REPRESENTATION</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Remove the witness from the lemma, since it isn't used and will
       cause confusion since the witness xml:ids will likely change,
       leaving this potentially wrong as well as unused. -->
  <xsl:template match="tei:lem/@wit" />

  <xsl:template match="tei:listWit" />

  <xsl:template match="tei:note/@target" />

  <xsl:template match="tei:rdg/@wit">
    <xsl:attribute name="wit">
      <xsl:for-each select="id(translate(., '#', ''))">
        <xsl:value-of select="." />
      </xsl:for-each>
    </xsl:attribute>
  </xsl:template>

  <xsl:template match="@resp">
    <xsl:attribute name="resp">
      <xsl:for-each select="id(translate(., '#', ''))">
        <xsl:text>{</xsl:text>
        <xsl:value-of select="tei:resp" />
        <xsl:text>|</xsl:text>
        <xsl:value-of select="tei:name" />
        <xsl:text>}</xsl:text>
      </xsl:for-each>
    </xsl:attribute>
  </xsl:template>

  <xsl:template match="tei:editionStmt/tei:respStmt" />

  <xsl:template match="cb:tt/@from" />
  <xsl:template match="cb:tt/@to" />

  <!-- Handling moving the apparatus criticus etc into the body. -->
  <xsl:template match="tei:*|text()">
    <xsl:variable name="beginning"
                  select="substring-after(preceding-sibling::tei:anchor[starts-with(@xml:id, 'beg')][1]/@xml:id, 'beg')" />
    <xsl:variable name="ending"
                  select="substring-after(following-sibling::tei:anchor[starts-with(@xml:id, 'end')][1]/@xml:id, 'end')" />
    <xsl:if test="not($beginning and $beginning = $ending)">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()" />
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <xsl:template match="@*|*">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()" />
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>